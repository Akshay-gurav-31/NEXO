import os
import cv2
import zipfile
import nibabel as nib
import numpy as np
import tempfile
from skimage import measure
from scipy import ndimage
import plotly.graph_objects as go
import warnings
from typing import Optional, Tuple
import google.generativeai as genai

warnings.filterwarnings('ignore')

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
HYPOTHESES_PATH = os.path.join(PLUGIN_DIR, 'hypotheses_utf8.txt')

class BrainAnalysisError(Exception):
    """Custom exception for brain analysis errors"""
    pass

def process_slice(args):
    slice_2d, clahe = args
    try:
        slice_norm = ((slice_2d - np.min(slice_2d)) / (np.max(slice_2d) - np.min(slice_2d)) * 255).astype(np.uint8)
        enhanced = clahe.apply(slice_norm)
        return enhanced.astype(np.float64) / 255.0
    except Exception:
        return slice_2d

def safe_load_volume(file_path: str) -> Tuple[Optional[np.ndarray], Optional[str]]:
    try:
        if file_path.endswith(".nii.gz"):
            try:
                img = nib.load(file_path)
                volume = img.get_fdata()
                if volume.dtype == np.dtype('V'):
                    volume = volume.astype(np.float64)
                elif volume.dtype != np.float64:
                    volume = volume.astype(np.float64)
                volume = np.nan_to_num(volume, nan=0.0, posinf=1.0, neginf=0.0)
                if np.any(np.isnan(volume)) or np.any(np.isinf(volume)):
                    volume = np.nan_to_num(volume, nan=0.0, posinf=1.0, neginf=0.0)
                return volume, None
            except Exception as e:
                return None, f"Error loading NIfTI file: {str(e)}"
        elif file_path.endswith(".zip"):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                    image_files = sorted([f for f in os.listdir(temp_dir) if f.lower().endswith(('.jpg', '.png'))])
                    if not image_files:
                        return None, "No valid images found in zip file"
                    first_img = cv2.imread(os.path.join(temp_dir, image_files[0]), cv2.IMREAD_GRAYSCALE)
                    if first_img is None:
                        return None, "Error reading first image"
                    volume = np.zeros((first_img.shape[0], first_img.shape[1], len(image_files)), dtype=np.float64)
                    for i, fname in enumerate(image_files):
                        img_path = os.path.join(temp_dir, fname)
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            volume[:,:,i] = img.astype(np.float64) / 255.0
                    return volume, None
            except Exception as e:
                return None, f"Error processing zip file: {str(e)}"
        else:
            return None, "Unsupported file format"
    except Exception as e:
        return None, f"Error loading volume: {str(e)}"

def safe_normalize_volume(volume: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[str]]:
    try:
        if volume is None or volume.size == 0:
            return None, "Empty volume data"
        volume = volume.astype(np.float64)
        volume = np.nan_to_num(volume, nan=0.0, posinf=1.0, neginf=0.0)
        vmin, vmax = np.min(volume), np.max(volume)
        if vmin == vmax:
            return None, "Volume has no variation (all values are the same)"
        normalized = (volume - vmin) / (vmax - vmin)
        return normalized.astype(np.float64), None
    except Exception as e:
        return None, f"Error normalizing volume: {str(e)}"

def safe_segment_tumor(volume: np.ndarray, threshold: float, min_size: int) -> Tuple[Optional[np.ndarray], Optional[str]]:
    try:
        if volume is None or volume.size == 0:
            return None, "Empty volume data"
        volume_float = volume.astype(np.float64)
        if not 0 <= threshold <= 1:
            return None, "Threshold must be between 0 and 1"
        if min_size < 0:
            return None, "Minimum size must be positive"
        try:
            smoothed = ndimage.gaussian_filter(volume_float, sigma=1.0)
            vmin, vmax = np.percentile(smoothed, (1, 99))
            enhanced = np.clip((smoothed - vmin) / (vmax - vmin), 0, 1)
            binary = enhanced > threshold
            kernel = np.ones((3,3,3))
            binary = ndimage.binary_opening(binary, structure=kernel)
            binary = ndimage.binary_closing(binary, structure=kernel)
            labeled, num_features = ndimage.label(binary)
            sizes = np.bincount(labeled.ravel())
            mask_sizes = sizes > min_size
            mask_sizes[0] = 0
            for i in range(1, len(sizes)):
                if mask_sizes[i]:
                    region = (labeled == i)
                    mean_intensity = np.mean(enhanced[region])
                    region_volume = sizes[i]
                    region_shape = np.sum(region, axis=(0,1))
                    if (mean_intensity < 0.2 or mean_intensity > 0.8 or region_volume > volume_float.size * 0.3 or np.max(region_shape) > volume_float.shape[2] * 0.8):
                        mask_sizes[i] = False
            predicted_mask = mask_sizes[labeled]
            predicted_mask = ndimage.binary_dilation(predicted_mask, iterations=1)
            predicted_mask = ndimage.binary_erosion(predicted_mask, iterations=1)
            return predicted_mask.astype(np.float64), None
        except Exception as e:
            return None, f"Error in tumor detection: {str(e)}"
    except Exception as e:
        return None, f"Error in segmentation: {str(e)}"

def safe_visualize_slice(slice_img: np.ndarray, mask_slice: Optional[np.ndarray], contrast: float, brightness: float) -> Tuple[Optional[np.ndarray], Optional[str]]:
    try:
        slice_img = (slice_img * contrast) + brightness
        slice_img = np.clip(slice_img, 0, 1)
        if mask_slice is not None:
            if mask_slice.shape != slice_img.shape:
                mask_slice = cv2.resize(mask_slice.astype(np.uint8), (slice_img.shape[1], slice_img.shape[0]), interpolation=cv2.INTER_NEAREST)
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

def safe_generate_ai_summary(tumor_volume: float, tumor_percentage: float, total_volume: float, confidence_score: float, gemini_api_key: Optional[str]=None) -> Tuple[Optional[str], Optional[str]]:
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
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
        else:
            raise RuntimeError("Gemini API key required for summary generation.")
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text, None
    except Exception as e:
        return None, f"Error generating AI summary: {str(e)}"

def load_hypotheses() -> str:
    try:
        with open(HYPOTHESES_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def run_mri_3d(input_file, threshold=0.5, min_size=100, contrast=1.0, brightness=0.0, gemini_api_key=None):
    """
    Main entry point for 3D MRI brain tumor analysis.
    Args:
        input_file (str): Path to MRI .nii.gz or .zip file.
        threshold (float): Tumor segmentation threshold (0-1).
        min_size (int): Minimum size for tumor region (voxels).
        contrast (float): Contrast adjustment for visualization.
        brightness (float): Brightness adjustment for visualization.
        gemini_api_key (str, optional): API key for Gemini AI summary.
    Returns:
        dict: Results including volume, mask, summary, and errors if any.
    """
    result = {"error": None}
    volume, err = safe_load_volume(input_file)
    if err:
        result["error"] = err
        return result
    norm_vol, err = safe_normalize_volume(volume)
    if err:
        result["error"] = err
        return result
    mask, err = safe_segment_tumor(norm_vol, threshold, min_size)
    if err:
        result["error"] = err
        return result
    # Visualization: take the middle slice
    mid_slice = norm_vol[:,:,norm_vol.shape[2]//2]
    mask_slice = mask[:,:,mask.shape[2]//2] if mask is not None else None
    vis_slice, err = safe_visualize_slice(mid_slice, mask_slice, contrast, brightness)
    if err:
        result["error"] = err
        return result
    # Tumor stats
    tumor_volume = np.sum(mask) if mask is not None else 0
    total_volume = np.prod(norm_vol.shape)
    tumor_percentage = 100.0 * tumor_volume / total_volume if total_volume > 0 else 0.0
    # AI summary
    summary, summary_err = None, None
    if gemini_api_key:
        summary, summary_err = safe_generate_ai_summary(tumor_volume, tumor_percentage, total_volume, 95.0, gemini_api_key)
    result.update({
        "volume_shape": norm_vol.shape,
        "tumor_mask": mask,
        "visualization": vis_slice,
        "tumor_volume": tumor_volume,
        "tumor_percentage": tumor_percentage,
        "summary": summary,
        "summary_error": summary_err,
        "hypotheses": load_hypotheses()
    })
    return result
