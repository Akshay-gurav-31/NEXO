import streamlit as st
import cv2
import zipfile
import os
import nibabel as nib
import numpy as np
import tempfile
from skimage import measure
import plotly.graph_objects as go
from scipy import ndimage
import google.generativeai as genai
import traceback
from typing import Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
import warnings
warnings.filterwarnings('ignore')

# Get the absolute path to the app directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))
HYPOTHESES_PATH = os.path.join(APP_DIR, 'hypotheses_utf8.txt')

# Load hypotheses at startup
try:
    with open(HYPOTHESES_PATH, 'r') as f:
        hypotheses = f.read()
except Exception as e:
    st.error(f"Error loading hypotheses: {str(e)}")
    hypotheses = ""

# Custom error handling class
class BrainAnalysisError(Exception):
    """Custom exception for brain analysis errors"""
    pass

def process_slice(args):
    """Process a single slice for parallel processing"""
    slice_2d, clahe = args
    try:
        # Normalize to 0-255 range
        slice_norm = ((slice_2d - np.min(slice_2d)) / (np.max(slice_2d) - np.min(slice_2d)) * 255).astype(np.uint8)
        # Apply CLAHE
        enhanced = clahe.apply(slice_norm)
        # Convert back to float64 and normalize
        return enhanced.astype(np.float64) / 255.0
    except Exception:
        return slice_2d

def safe_load_volume(file_path: str) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """Safely load volume data from file with proper type conversion"""
    try:
        if file_path.endswith(".nii.gz"):
            try:
                # Load NIfTI file
                img = nib.load(file_path)
                # Get data and ensure it's float64
                volume = img.get_fdata()
                
                # Handle different data types
                if volume.dtype == np.dtype('V'):  # Void type
                    volume = volume.astype(np.float64)
                elif volume.dtype != np.float64:
                    volume = volume.astype(np.float64)
                
                # Handle any invalid values
                volume = np.nan_to_num(volume, nan=0.0, posinf=1.0, neginf=0.0)
                
                # Ensure the data is in a valid range
                if np.any(np.isnan(volume)) or np.any(np.isinf(volume)):
                    volume = np.nan_to_num(volume, nan=0.0, posinf=1.0, neginf=0.0)
                
                return volume, None
                
            except Exception as e:
                return None, f"Error loading NIfTI file: {str(e)}"
                
        elif file_path.endswith(".zip"):
            try:
                # Create temporary directory for extraction
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Extract zip file
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    
                    # Get list of image files
                    image_files = sorted([f for f in os.listdir(temp_dir) 
                                       if f.lower().endswith(('.jpg', '.png'))])
                    
                    if not image_files:
                        return None, "No valid images found in zip file"
                    
                    # Read first image to get dimensions
                    first_img = cv2.imread(os.path.join(temp_dir, image_files[0]), 
                                         cv2.IMREAD_GRAYSCALE)
                    if first_img is None:
                        return None, "Error reading first image"
                    
                    # Create empty volume array with float64 type
                    volume = np.zeros((first_img.shape[0], first_img.shape[1], 
                                     len(image_files)), dtype=np.float64)
                    
                    # Read and process each image
                    for i, fname in enumerate(image_files):
                        img_path = os.path.join(temp_dir, fname)
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            # Convert to float64 and normalize to 0-1
                            volume[:,:,i] = img.astype(np.float64) / 255.0
                    
                    return volume, None
                    
            except Exception as e:
                return None, f"Error processing zip file: {str(e)}"
        else:
            return None, "Unsupported file format"
            
    except Exception as e:
        return None, f"Error loading volume: {str(e)}"

def safe_normalize_volume(volume: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """Safely normalize volume data with proper type handling"""
    try:
        if volume is None or volume.size == 0:
            return None, "Empty volume data"
        
        # Ensure volume is float64
        volume = volume.astype(np.float64)
        
        # Handle invalid values
        volume = np.nan_to_num(volume, nan=0.0, posinf=1.0, neginf=0.0)
        
        # Check if volume is constant
        vmin, vmax = np.min(volume), np.max(volume)
        if vmin == vmax:
            return None, "Volume has no variation (all values are the same)"
        
        # Normalize to 0-1 range
        normalized = (volume - vmin) / (vmax - vmin)
        return normalized.astype(np.float64), None
        
    except Exception as e:
        return None, f"Error normalizing volume: {str(e)}"

def safe_segment_tumor(volume: np.ndarray, threshold: float, min_size: int) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """Advanced brain tumor segmentation for 3D MRI"""
    try:
        if volume is None or volume.size == 0:
            return None, "Empty volume data"
        
        # Ensure volume is float64
        volume_float = volume.astype(np.float64)
        
        # Validate parameters
        if not 0 <= threshold <= 1:
            return None, "Threshold must be between 0 and 1"
        if min_size < 0:
            return None, "Minimum size must be positive"
        
        try:
            # 1. Brain-specific preprocessing
            smoothed = ndimage.gaussian_filter(volume_float, sigma=1.0)
            
            # 2. Brain-specific normalization
            vmin, vmax = np.percentile(smoothed, (1, 99))
            enhanced = np.clip((smoothed - vmin) / (vmax - vmin), 0, 1)
            
            # 3. Brain-specific tumor detection
            binary = enhanced > threshold
            
            # 4. Brain-specific morphological operations
            kernel = np.ones((3,3,3))
            binary = ndimage.binary_opening(binary, structure=kernel)
            binary = ndimage.binary_closing(binary, structure=kernel)
            
            # 5. Connected component analysis
            labeled, num_features = ndimage.label(binary)
            sizes = np.bincount(labeled.ravel())
            mask_sizes = sizes > min_size
            mask_sizes[0] = 0  # Remove background
            
            # 6. Brain-specific filtering
            for i in range(1, len(sizes)):
                if mask_sizes[i]:
                    region = (labeled == i)
                    mean_intensity = np.mean(enhanced[region])
                    region_volume = sizes[i]
                    region_shape = np.sum(region, axis=(0,1))
                    
                    if (mean_intensity < 0.2 or 
                        mean_intensity > 0.8 or 
                        region_volume > volume_float.size * 0.3 or 
                        np.max(region_shape) > volume_float.shape[2] * 0.8):
                        mask_sizes[i] = False
            
            # 7. Create final mask
            predicted_mask = mask_sizes[labeled]
            
            # 8. Final cleanup
            predicted_mask = ndimage.binary_dilation(predicted_mask, iterations=1)
            predicted_mask = ndimage.binary_erosion(predicted_mask, iterations=1)
            
            return predicted_mask.astype(np.float64), None
            
        except Exception as e:
            return None, f"Error in tumor detection: {str(e)}"
            
    except Exception as e:
        return None, f"Error in segmentation: {str(e)}"

def safe_visualize_slice(slice_img: np.ndarray, mask_slice: Optional[np.ndarray], 
                        contrast: float, brightness: float) -> Tuple[Optional[np.ndarray], Optional[str]]:
    """Safely visualize slice with mask overlay"""
    try:
        slice_img = (slice_img * contrast) + brightness
        slice_img = np.clip(slice_img, 0, 1)
        
        if mask_slice is not None:
            if mask_slice.shape != slice_img.shape:
                mask_slice = cv2.resize(mask_slice.astype(np.uint8), 
                                      (slice_img.shape[1], slice_img.shape[0]), 
                                      interpolation=cv2.INTER_NEAREST)
            
            mask_slice = mask_slice.astype(bool)
            colored_slice = cv2.cvtColor((slice_img * 255).astype(np.uint8), cv2.COLOR_GRAY2RGB)
            masked_slice = colored_slice.copy()
            masked_slice[mask_slice] = [255, 0, 0]
            alpha = 0.7
            colored_slice = cv2.addWeighted(colored_slice, 1-alpha, masked_slice, alpha, 0)
            return colored_slice, None
        else:
            return (slice_img * 255).astype(np.uint8), None
    except Exception as e:
        return None, f"Error in slice visualization: {str(e)}"

def safe_marching_cubes(data: np.ndarray, level: float) -> Tuple[Optional[Tuple], Optional[str]]:
    """Safely perform marching cubes with error handling"""
    try:
        if data is None or data.size == 0:
            return None, "Empty data for marching cubes"
        
        data = data.astype(np.float64)
        levels = [level, 0.3, 0.7, 0.1, 0.9]
        for l in levels:
            try:
                result = measure.marching_cubes(data, level=l)
                return result, None
            except ValueError:
                continue
        return None, "Could not generate surface with any level"
    except Exception as e:
        return None, f"Error in marching cubes: {str(e)}"

def safe_generate_ai_summary(tumor_volume: float, tumor_percentage: float, 
                           total_volume: float, confidence_score: float) -> Tuple[Optional[str], Optional[str]]:
    """Safely generate AI summary with error handling"""
    try:
        prompt = f"""
        Based on the following brain MRI analysis results, provide a concise medical summary:
        - Tumor Volume: {tumor_volume:,.0f} voxels
        - Tumor Percentage: {tumor_percentage:.2f}%
        - Total Brain Volume: {total_volume:,.0f} voxels
        - Detection Confidence: {confidence_score:.1f}%

        Please provide:
        1. A brief interpretation of these results
        2. Potential clinical significance
        3. Recommended next steps
        Keep the response professional and medical-focused.
        """
        
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text, None
    except Exception as e:
        return None, f"Error generating AI summary: {str(e)}"

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')

# Set page config for better mobile experience
st.set_page_config(
    page_title="MRIxAI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for responsive design
st.markdown("""
<style>
    .stApp {
        max-width: 100%;
        padding: 0.5rem;
    }
    h1 {
        font-size: clamp(1.5rem, 4vw, 2.5rem);
        text-align: center;
        margin: 1rem 0;
    }
    h2 {
        font-size: clamp(1.2rem, 3vw, 2rem);
    }
    h3 {
        font-size: clamp(1rem, 2.5vw, 1.5rem);
    }
    .css-1d391kg {
        padding: 1rem 0.5rem;
    }
    .stSlider {
        width: 100%;
    }
    .stButton>button {
        width: 100%;
        margin: 0.5rem 0;
    }
    .stMetric {
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.5rem;
        font-size: clamp(0.8rem, 2vw, 1rem);
    }
    .stPlotlyChart {
        position: relative;
        width: 100%;
        height: 500px !important;
        border: 2px solid #ff0000;
        border-radius: 8px;
        overflow: hidden;
        margin: 1rem 0;
        background: #f8f9fa;
    }
    .stPlotlyChart::before {
        content: '';
        position: absolute;
        top: -100vh;
        left: -100vw;
        right: -100vw;
        bottom: -100vh;
        z-index: -1;
        background: transparent;
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 0.25rem;
        }
        .stSidebar {
            padding: 0.25rem;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.25rem;
        }
        .row-widget.stButton {
            width: 100%;
        }
        .stMetric {
            padding: 0.25rem;
        }
        .element-container:not(:has(.stPlotlyChart)) {
            pointer-events: auto;
        }
        .stTabs [data-baseweb="tab-panel"] {
            padding: 0.5rem;
        }
        .stPlotlyChart {
            height: 400px !important;
            margin: 0.5rem 0;
        }
    }
    @media (min-width: 769px) and (max-width: 1024px) {
        .stApp {
            padding: 0.5rem;
        }
    }
    @media (min-width: 1025px) {
        .stApp {
            padding: 1rem;
        }
    }
    button, select, input {
        min-height: 44px;
    }
    .element-container {
        margin: 0.5rem 0;
    }
    .stMarkdown {
        color: inherit;
    }
    .row-widget.stHorizontal {
        flex-wrap: wrap;
    }
    .stSidebar .sidebar-content {
        padding: 0.5rem;
    }
    .back-button {
        background-color: #f63366;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
    }
    .back-button:hover {
        background-color: #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown("<h1>🧠 MRIxAI</h1>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 📱 Brain MRI Analysis")
    st.markdown("---")
    st.markdown("#### 📤 Upload MRI")
    uploaded_file = st.file_uploader(
        "Select Brain MRI (.nii.gz or .zip)",
        type=["nii.gz", "zip"],
        help="Upload your brain MRI scan for analysis",
        key="file_uploader"
    )
    st.markdown("#### 🔍 Detection Parameters")
    threshold = st.slider(
        "Detection Sensitivity",
        min_value=0.0,
        max_value=1.0,
        value=0.65,
        step=0.01,
        help="Higher values detect brighter regions. Recommended: 0.6-0.7"
    )
    min_size = st.slider(
        "Minimum Tumor Size",
        min_value=50,
        max_value=500,
        value=100,
        step=10,
        help="Minimum size of tumor regions (voxels). Recommended: 100-200"
    )
    st.markdown("#### 📊 Results")
    col1, col2 = st.columns(2)
    with col1:
        tumor_volume_placeholder = st.empty()
        tumor_percentage_placeholder = st.empty()
    with col2:
        confidence_score_placeholder = st.empty()
    
# Updated Back to Home button with new URL
st.markdown("""
    <input type="hidden" id="homeUrl" value="https://nexo-xadw.onrender.com/">
    <a href="https://nexo-xadw.onrender.com/" class="back-button" style="
        display: inline-block;
        padding: 8px 16px;
        background-color: #4CAF50;
        color: white;
        text-decoration: none;
        border-radius: 5px;
        font-weight: 600;
    ">Back to Home</a>
""", unsafe_allow_html=True)

# Main content
if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            with st.spinner("Processing MRI..."):
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                volume, error = safe_load_volume(file_path)
                if error:
                    st.error(f"Error loading MRI: {error}")
                    st.stop()
                
                volume, error = safe_normalize_volume(volume)
                if error:
                    st.error(f"Error processing MRI: {error}")
                    st.stop()
                
                st.success("✅ MRI loaded successfully")
                
                predicted_mask, error = safe_segment_tumor(volume, threshold, min_size)
                if error:
                    st.error(f"Error in tumor detection: {error}")
                    st.stop()
            
            st.session_state['predicted_mask'] = predicted_mask
            
            tumor_volume = np.sum(predicted_mask)
            total_volume = volume.shape[0] * volume.shape[1] * volume.shape[2]
            tumor_percentage = (tumor_volume / total_volume) * 100 if total_volume > 0 else 0
            
            tumor_size = None
            tumor_center = None
            if tumor_volume > 0:
                tumor_mask_bool = predicted_mask.astype(bool)
                tumor_coords = np.where(tumor_mask_bool)
                if tumor_coords[0].size > 0:
                    tumor_size = [np.max(coord) - np.min(coord) + 1 for coord in tumor_coords]
                    tumor_center = [np.mean(coord) for coord in tumor_coords]
            
            tumor_volume_placeholder.metric(
                "Tumor Volume",
                f"{tumor_volume:,.0f} voxels",
                help="Total volume of detected tumor regions"
            )
            tumor_percentage_placeholder.metric(
                "Tumor Percentage",
                f"{tumor_percentage:.2f}%",
                help="Percentage of total brain volume"
            )
            confidence_score_placeholder.metric(
                "Confidence",
                f"{(1 - threshold) * 100:.1f}%",
                help="Detection confidence level"
            )
            
            st.session_state.update({
                'tumor_volume': tumor_volume,
                'tumor_percentage': tumor_percentage,
                'total_volume': total_volume,
                'tumor_size': tumor_size,
                'tumor_center': tumor_center
            })
            
            tab1, tab2, tab3, tab4 = st.tabs([
                "🧊 3D View",
                "📊 Slices",
                "🔍 Details",
                "👨‍⚕️ Summary"
            ])
            
            with tab1:
                st.subheader("🧊 3D View")
                try:
                    with st.container():
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            brain_opacity = st.slider("Brain Opacity", 0.0, 1.0, 0.2, 0.1)
                            brain_color = st.color_picker("Brain Color", "#ADD8E6")
                        with col2:
                            tumor_opacity = st.slider("Tumor Opacity", 0.0, 1.0, 0.6, 0.1)
                            tumor_color = st.color_picker("Tumor Color", "#FF0000")
                        with col3:
                            show_axes = st.checkbox("Show Axes", value=True)
                            show_legend = st.checkbox("Show Legend", value=True)

                        brain_result, error = safe_marching_cubes(volume, 0.5)
                        if error:
                            st.error(error)
                            st.stop()
                        
                        verts, faces, _, _ = brain_result
                        
                        fig = go.Figure()
                        fig.add_trace(go.Mesh3d(
                            x=verts[:, 0], y=verts[:, 1], z=verts[:, 2],
                            i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
                            color=brain_color, opacity=brain_opacity, name="Brain",
                            showscale=False
                        ))

                        if predicted_mask is not None and np.any(predicted_mask):
                            tumor_result, error = safe_marching_cubes(predicted_mask, 0.5)
                            if not error:
                                tumor_verts, tumor_faces, _, _ = tumor_result
                                fig.add_trace(go.Mesh3d(
                                    x=tumor_verts[:, 0], y=tumor_verts[:, 1], z=tumor_verts[:, 2],
                                    i=tumor_faces[:, 0], j=tumor_faces[:, 1], k=tumor_faces[:, 2],
                                    color=tumor_color, opacity=tumor_opacity, name="Predicted Tumor",
                                    showscale=False
                                ))

                        fig.update_layout(
                            scene=dict(
                                xaxis_title='Right-Left',
                                yaxis_title='Anterior-Posterior',
                                zaxis_title='Superior-Inferior',
                                aspectmode='data',
                                camera=dict(
                                    up=dict(x=0, y=0, z=1),
                                    center=dict(x=0, y=0, z=0),
                                    eye=dict(x=1.5, y=1.5, z=1.5)
                                )
                            ),
                            margin=dict(l=0, r=0, b=0, t=0),
                            showlegend=show_legend,
                            height=500,
                            width=None,
                            scene_aspectmode='data',
                            dragmode='orbit',
                            hovermode='closest',
                            uirevision='constant'
                        )

                        fig.update_scenes(
                            xaxis_visible=show_axes,
                            yaxis_visible=show_axes,
                            zaxis_visible=show_axes,
                            xaxis=dict(title=dict(text="Right-Left"), showgrid=True, zeroline=True),
                            yaxis=dict(title=dict(text="Anterior-Posterior"), showgrid=True, zeroline=True),
                            zaxis=dict(title=dict(text="Superior-Inferior"), showgrid=True, zeroline=True)
                        )

                        st.plotly_chart(fig, use_container_width=True, config={
                            'displayModeBar': True,
                            'scrollZoom': True,
                            'displaylogo': False,
                            'modeBarButtonsToAdd': ['orbitRotation', 'resetCamera'],
                            'modeBarButtonsToRemove': ['lasso2d', 'select2d']
                        })
                except Exception as e:
                    st.error(f"Error in 3D visualization: {str(e)}")
                    st.info("Try adjusting the visualization parameters.")
            
            with tab2:
                st.subheader("📊 Slices")
                try:
                    col1, col2 = st.columns(2)
                    with col1:
                        max_slice_idx = volume.shape[2] - 1
                        slice_idx = st.slider("Slice Index", 0, max_slice_idx, min( volume.shape[2] // 2, max_slice_idx))
                        contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1)
                    with col2:
                        brightness = st.slider("Brightness", -1.0, 1.0, 0.0, 0.1)
                        show_mask = st.checkbox("Show Tumor Mask", value=True)

                    slice_img = volume[:, :, slice_idx]
                    mask_slice = predicted_mask[:, :, slice_idx] if predicted_mask is not None else None
                    
                    result, error = safe_visualize_slice(slice_img, mask_slice, contrast, brightness)
                    if error:
                        st.error(error)
                    else:
                        st.image(result, caption=f"Slice {slice_idx}")
                except Exception as e:
                    st.error(f"Error in slice analysis: {str(e)}")
            
            with tab3:
                st.subheader("🔍 Details")
                if 'tumor_volume' in st.session_state and predicted_mask is not None:
                    st.write("Tumor Statistics")
                    tumor_mask_bool = predicted_mask.astype(bool)
                    try:
                        num_regions = len(np.unique(predicted_mask)) - 1
                        if num_regions < 0:
                            num_regions = 0
                        
                        if np.any(tumor_mask_bool):
                            avg_intensity = np.mean(volume[tumor_mask_bool])
                            max_intensity = np.max(volume[tumor_mask_bool])
                        else:
                            avg_intensity = 0
                            max_intensity = 0
                        
                        st.write(f"- Number of tumor regions: {num_regions}")
                        st.write(f"- Average tumor intensity: {avg_intensity:.3f}")
                        st.write(f"- Maximum tumor intensity: {max_intensity:.3f}")
                        
                        st.write("Volume Statistics")
                        st.write(f"- Total volume: {total_volume:,.0f} voxels")
                        st.write(f"- Tumor volume: {tumor_volume:,.0f} voxels")
                        st.write(f"- Tumor percentage: {tumor_percentage:.2f}%")
                        
                        if np.any(tumor_mask_bool):
                            tumor_coords = np.where(tumor_mask_bool)
                            tumor_size = [np.max(coord) - np.min(coord) for coord in tumor_coords]
                            st.write("\nTumor Dimensions (voxels):")
                            st.write(f"- X: {tumor_size[0]:.0f}")
                            st.write(f"- Y: {tumor_size[1]:.0f}")
                            st.write(f"- Z: {tumor_size[2]:.0f}")
                            
                            tumor_center = [np.mean(coord) for coord in tumor_coords]
                            st.write("\nTumor Center (voxels):")
                            st.write(f"- X: {tumor_center[0]:.1f}")
                            st.write(f"- Y: {tumor_center[1]:.1f}")
                            st.write(f"- Z: {tumor_center[2]:.1f}")
                    except Exception as e:
                        st.error(f"Error calculating tumor statistics: {str(e)}")
                    
                    st.markdown("### Initial Hypotheses")
                    if hypotheses:
                        formatted_hypotheses = hypotheses.replace('\n', '  \n')
                        st.markdown(formatted_hypotheses, unsafe_allow_html=True)
                    else:
                        st.warning("Could not load hypotheses.")
                else:
                    st.info("Tumor details will be shown here after processing an MRI scan.")
            
            with tab4:
                st.subheader("👨‍⚕️ AI Doctor Summary")
                try:
                    if 'tumor_volume' in st.session_state:
                        summary, error = safe_generate_ai_summary(
                            st.session_state['tumor_volume'],
                            st.session_state['tumor_percentage'],
                            st.session_state['total_volume'],
                            (1 - threshold) * 100
                        )
                        if error:
                            st.error(error)
                        else:
                            st.markdown("### AI-Generated Medical Summary")
                            st.markdown(summary)
                            st.markdown("""
                            ---
                            *Disclaimer: This AI-generated summary is for informational purposes only and should not be considered as medical advice. Please consult with a qualified healthcare professional for proper medical interpretation and guidance.*
                            """)
                    else:
                        st.info("Please upload and analyze an MRI scan to generate an AI summary.")
                except Exception as e:
                    st.error(f"Error in AI summary generation: {str(e)}")
        except Exception as e:
            st.error(f"Error processing MRI: {str(e)}")
else:
    st.info("Please upload an MRI file to begin analysis.")
