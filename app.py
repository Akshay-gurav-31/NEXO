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
import sys # Import sys to use st.stop()
import google.generativeai as genai # Import the generativeai library
# import openai # Uncomment and install if using OpenAI
# from transformers import pipeline # Uncomment and install if using HuggingFace

# Set page config for better layout
st.set_page_config(
    page_title=" DeepBrainDx Ai",
    page_icon="🧠",
    layout="wide" # Use wide layout for sidebar on desktop
)

st.title("━━━━⊱DeepBrainDx AI⊰━━━━")

# Custom CSS for better mobile experience and layout, anSd theme support
st.markdown("""
<style>
    /* Base styles (for dark theme or default) */
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        background-color: #121212; /* Ensure dark background */
        color: #ffffff; /* Ensure light text */
    }
    h1, h2, h3 {
        color: #fff;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        text-align: center;
        margin-top: 3rem;
    }
    .stApp {
        max-width: none; /* Allow wide layout */
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .stFileUploader {
        width: 100%;
    }
    .stPlotlyChart {
        width: 100%;
        height: 600px !important; /* Adjust height as needed */
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        /* max-width removed to work with wide layout */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e1e1e;
        border-radius: 4px 4px 0 0;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2e2e2e;
    }
    @media (max-width: 768px) {
        .stApp {
            padding: 0.5rem;
        }
    }
    /* Style for the sidebar */
    .stSidebar {
        padding-top: 2rem;
        background-color: #1e1e1e; /* Dark background for sidebar */
        color: #ffffff; /* Light text for sidebar */
    }
    .stSidebar .stSubheader {
        color: #ffffff; /* Ensure subheaders are visible */
    }

    /* --- Styles for Light Theme --- */
    [data-theme="light"] body {
        background-color: #ffffff; /* Light background */
        color: #000000; /* Black text */
    }
    [data-theme="light"] h1, [data-theme="light"] h2, [data-theme="light"] h3 {
        color: #000; /* Already black */
        text-shadow: none;
    }
    [data-theme="light"] .stSidebar {
        background-color: #f0f2f6; /* Light background for sidebar */
        color: #000000; /* Black text for sidebar */
    }
     [data-theme="light"] .stSidebar .stSubheader {
        color: #000000; /* Ensure subheaders are visible and black */
    }
     [data-theme="light"] .stTabs [data-baseweb="tab"] {
        background-color: #e0e0e0; /* Lighter background for tabs */
        color: #000000; /* Black text for tabs */
    }
     [data-theme="light"] .stTabs [aria-selected="true"] {
        background-color: #ffffff; /* White background for active tab */
        color: #000000; /* Black text for active tab */
    }
     [data-theme="light"] input[type="file"],
     [data-theme="light"] input[type="submit"] {
        background-color: #f0f0f0; /* Light background for inputs */
        color: #000000; /* Black text for inputs */
        border: 1px solid #ccc; /* Lighter border */
    }
     [data-theme="light"] input[type="submit"] {
        background-color: #007bff; /* Keep primary color for submit */
        color: #fff; /* White text for submit */
    }
     [data-theme="light"] input[type="submit"]:hover {
        background-color: #0056b3; /* Darker hover */
    }

</style>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.subheader("Upload MRI")
    # Step 1: Upload
    uploaded_file = st.file_uploader("Select MRI (.nii.gz or .zip of slices)", type=["nii.gz", "zip"])

    st.subheader("Tumor Detection Controls")
    # Add detection parameters
    threshold = st.slider("Detection Threshold", 0.0, 1.0, 0.8, 0.01, key='detection_threshold') # Added key for session state
    min_size = st.slider("Minimum Tumor Size (voxels)", 10, 1000, 100, key='min_tumor_size') # Added key for session state

    # Display statistics in sidebar - will be updated after file upload
    st.subheader("Tumor Statistics")
    # These will be populated later in the main content block
    tumor_volume_placeholder = st.empty()
    tumor_percentage_placeholder = st.empty()
    confidence_score_placeholder = st.empty()

# --- Main Content ---
# The rest of the app logic and visualization will be here

if uploaded_file:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        volume = None # Initialize volume to None
        try:
            # Step 2: Load Volume
            if file_path.endswith(".nii.gz"):
                img = nib.load(file_path)
                volume = img.get_fdata()
            elif file_path.endswith(".zip"):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                slices = []
                # Collect image files from extracted directory
                for fname in sorted(os.listdir(temp_dir)):
                    if fname.lower().endswith(('.jpg', '.png')):
                        img_path = os.path.join(temp_dir, fname)
                        try:
                            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                            if img is not None:
                                slices.append(img)
                            else:
                                st.warning(f"Could not read image file: {fname}")
                        except Exception as e:
                            st.warning(f"Error reading image file {fname}: {e}")

                if not slices:
                    st.error("The uploaded zip file does not contain any valid .jpg or .png images.")
                    st.stop() # Stop execution if no slices found

                # Stack slices into a volume
                volume = np.stack(slices, axis=-1)

            # Check if volume was loaded successfully
            if volume is None:
                 st.error("Could not load volume from the uploaded file. Please check the file format.")
                 st.stop()

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
            st.stop() # Stop execution on file processing errors


        # Step 3: Normalize volume (only if volume is loaded)
        if volume is not None:
            volume = (volume - np.min(volume)) / (np.max(volume) - np.min(volume))

            st.success(f"Volume Loaded. Shape: {volume.shape}")

            # --- Advanced Tumor Segmentation Placeholder ---
            # In a real application, you would integrate your U-Net model here.
            # This would take 'volume' as input and output 'predicted_mask'.
            # For now, we use the thresholding method.
            def perform_advanced_segmentation(volume, threshold, min_size):
                 # Replace this with your U-Net inference code
                 # Example: loaded_model.predict(volume)
                 # For now, using the thresholding logic with passed parameters
                 binary = volume > threshold
                 binary = ndimage.binary_opening(binary)
                 binary = ndimage.binary_closing(binary)
                 labeled, num_features = ndimage.label(binary)
                 sizes = np.bincount(labeled.ravel())
                 mask_sizes = sizes > min_size
                 mask_sizes[0] = 0
                 predicted_mask = mask_sizes[labeled]
                 return predicted_mask

            # Pass threshold and min_size from sidebar to segmentation function
            predicted_mask = perform_advanced_segmentation(volume, threshold, min_size)
            st.session_state['predicted_mask'] = predicted_mask # Store mask in session state


            # Calculate tumor statistics
            tumor_volume = np.sum(predicted_mask)
            total_volume = volume.shape[0] * volume.shape[1] * volume.shape[2]
            tumor_percentage = (tumor_volume / total_volume) * 100

            # Update statistics in sidebar
            tumor_volume_placeholder.metric("Tumor Volume (voxels)", f"{tumor_volume:,.0f}")
            tumor_percentage_placeholder.metric("Tumor Percentage", f"{tumor_percentage:.2f}%")
            confidence_score_placeholder.metric("Confidence Score", f"{(1 - threshold) * 100:.1f}%")

            # Store statistics in session state for access in AI Doctor Summary tab
            st.session_state['tumor_volume'] = tumor_volume
            st.session_state['tumor_percentage'] = tumor_percentage
            st.session_state['total_volume'] = total_volume


            # Create tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["3D Visualization", "Slice Analysis", "Tumor Detection Details", "AI Doctor Summary"])

            with tab1:
                st.subheader("🧊 3D Visualization")
                
                # Advanced visualization controls
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

                # Generate 3D visualization
                verts, faces, _, _ = measure.marching_cubes(volume, level=0.5)
                tumor_verts, tumor_faces, _, _ = measure.marching_cubes(predicted_mask, level=0.5)

                fig = go.Figure()

                # Add brain mesh
                fig.add_trace(go.Mesh3d(
                    x=verts[:, 0], y=verts[:, 1], z=verts[:, 2],
                    i=faces[:, 0], j=faces[:, 1], k=faces[:, 2],
                    color=brain_color, opacity=brain_opacity, name="Brain",
                    showscale=False
                ))

                # Add tumor mesh
                fig.add_trace(go.Mesh3d(
                    x=tumor_verts[:, 0], y=tumor_verts[:, 1], z=tumor_verts[:, 2],
                    i=tumor_faces[:, 0], j=tumor_faces[:, 1], k=tumor_faces[:, 2],
                    color=tumor_color, opacity=tumor_opacity, name="Predicted Tumor",
                    showscale=False
                ))

                # Enhanced layout
                fig.update_layout(
                    scene=dict(
                        xaxis_title='X',
                        yaxis_title='Y',
                        zaxis_title='Z',
                        aspectmode='data',
                        camera=dict(
                            up=dict(x=0, y=0, z=1),
                            center=dict(x=0, y=0, z=0),
                            eye=dict(x=1.5, y=1.5, z=1.5)
                        )
                    ),
                    margin=dict(l=0, r=0, b=0, t=0),
                    showlegend=show_legend,
                    height=600, # Adjusted height
                    width=None,
                    scene_aspectmode='data'
                )

                # Update axes visibility
                fig.update_scenes(
                    xaxis_visible=show_axes,
                    yaxis_visible=show_axes,
                    zaxis_visible=show_axes
                )

                st.plotly_chart(fig, use_container_width=True)

            with tab2:
                st.subheader("📊 Slice Analysis")
                
                # Slice viewer with advanced controls
                col1, col2 = st.columns(2)
                with col1:
                    # Ensure slice_idx is within bounds
                    max_slice_idx = volume.shape[2]-1
                    slice_idx = st.slider("Slice Index", 0, max_slice_idx, min(volume.shape[2]//2, max_slice_idx))
                    contrast = st.slider("Contrast", 0.0, 2.0, 1.0, 0.1)
                with col2:
                    brightness = st.slider("Brightness", -1.0, 1.0, 0.0, 0.1)
                    show_mask = st.checkbox("Show Tumor Mask", value=True)

                # Process slice
                slice_img = volume[:,:,slice_idx]
                slice_img = (slice_img * contrast) + brightness
                slice_img = np.clip(slice_img, 0, 1)

                if show_mask:
                    # Retrieve mask from session state if available
                    mask_slice = st.session_state.get('predicted_mask', None)
                    if mask_slice is not None and slice_idx < mask_slice.shape[2]:
                        mask_slice = mask_slice[:,:,slice_idx]
                        # Ensure mask_slice has the same dimensions as slice_img for np.where
                        if mask_slice.shape != slice_img.shape:
                             mask_slice = cv2.resize(mask_slice.astype(np.uint8), (slice_img.shape[1], slice_img.shape[0]), interpolation = cv2.INTER_NEAREST)
                             mask_slice = mask_slice.astype(bool)
                             
                        # Blend original slice with red where mask is True
                        colored_slice = cv2.cvtColor((slice_img * 255).astype(np.uint8), cv2.COLOR_GRAY2RGB)
                        colored_slice[mask_slice] = [255, 0, 0] # Red color for tumor mask
                        st.image(colored_slice, caption=f"Slice {slice_idx} with Tumor Mask")
                    else:
                         st.image(slice_img, caption=f"Slice {slice_idx}")
                         st.warning("Tumor mask not available for this slice or not generated.")

                else:
                    st.image(slice_img, caption=f"Slice {slice_idx}")

            with tab3:
                st.subheader("🔍 Tumor Detection Details")
                
                # Advanced tumor analysis
                st.write("Tumor Statistics")
                # Check if tumor_volume is calculated (i.e., a file was uploaded and processed)
                if 'tumor_volume' in st.session_state and st.session_state.get('tumor_volume', 0) > 0:
                     st.write(f"- Number of tumor regions: {len(np.unique(predicted_mask)) - 1}")
                     st.write(f"- Average tumor intensity: {np.mean(volume[predicted_mask]):.3f}")
                     st.write(f"- Maximum tumor intensity: {np.max(volume[predicted_mask]):.3f}")
                     st.write("Volume Statistics")
                     st.write(f"- Total volume: {total_volume:,.0f} voxels")
                     st.write(f"- Tumor volume: {tumor_volume:,.0f} voxels")
                     st.write(f"- Tumor percentage: {tumor_percentage:.2f}%")
                else:
                     st.write("No tumor detected or file not uploaded/processed.")

            with tab4:
                st.subheader("AI Doctor Summary")
                
                # --- Gemini LLM Integration ---
                # You would use the tumor statistics and potentially other findings
                # to create a prompt for the Gemini model.
                
                try:
                    # Ensure API key is available
                    api_key = st.secrets["GEMINI_API_KEY"]
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-2.0-flash')

                    # Get statistics from session state
                    current_tumor_volume = st.session_state.get('tumor_volume', 0)
                    current_tumor_percentage = st.session_state.get('tumor_percentage', 0)
                    # You would also need to add code to determine tumor location(s) if possible
                    # For now, let's include basic stats in the prompt.
                    
                    if current_tumor_volume > 0:
                        st.write("Generating a radiology-style report using LLLM Model...")
                        prompt = f"Generate a concise radiology report summary based on the following MRI analysis findings:\n\nTumor Volume: {current_tumor_volume:,.0f} voxels\nTumor Percentage of Total Volume: {current_tumor_percentage:.2f}%\n\nInclude sections for Findings, Impression, and Recommendation. Assume this is a brain MRI and the detected area is a potential tumor. Format the report clearly with headings and bullet points." # Refined prompt
                        
                        response = model.generate_content(prompt)
                        llm_report = response.text
                        
                        # Use st.markdown to render the report with formatting
                        st.markdown(llm_report)
                        
                    else:
                         st.info("Upload an MRI file and ensure a tumor is detected to generate a report.")

                except KeyError:
                    st.error("Gemini API key not found in Streamlit secrets. Please add it to .streamlit/secrets.toml")
                except Exception as e:
                    st.error(f"Error generating report with Gemini: {e}")
                
                st.info("Note: This report is AI-generated and should not be used for clinical decisions. Always consult with a qualified medical professional.")
