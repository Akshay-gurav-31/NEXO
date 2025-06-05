import nibabel as nib
import numpy as np
import pyvista as pv
import tkinter as tk
from tkinter import filedialog

# Step 1: File upload dialog to select the .nii.gz file
def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select MRI .nii.gz file",
        filetypes=[("NIfTI files", "*.nii.gz"), ("All files", "*.*")]
    )
    if not file_path:
        raise FileNotFoundError("No file selected. Please select a .nii.gz file.")
    return file_path

# Step 2: Load the MRI .nii.gz file
def load_mri(file_path):
    img = nib.load(file_path)
    data = img.get_fdata()
    return data

# Step 3: Segment the tumor (placeholder with thresholding)
def segment_tumor(mri_data, threshold=0.8):
    norm_data = (mri_data - np.min(mri_data)) / (np.max(mri_data) - np.min(mri_data))
    tumor_mask = norm_data > threshold
    return tumor_mask.astype(np.uint8)

# Step 4: PyVista 3D Visualization
def render_3d_pyvista(mri_data, tumor_mask):
    from skimage import measure
    # Normalize for surface extraction
    norm_data = (mri_data - np.min(mri_data)) / (np.max(mri_data) - np.min(mri_data))
    # Brain surface
    brain_verts, brain_faces, _, _ = measure.marching_cubes(norm_data, level=0.3)
    brain_faces = np.hstack([np.full((brain_faces.shape[0], 1), 3), brain_faces]).astype(np.int32)
    brain_mesh = pv.PolyData(brain_verts, brain_faces)
    # Tumor surface
    tumor_verts, tumor_faces, _, _ = measure.marching_cubes(tumor_mask, level=0.5)
    tumor_faces = np.hstack([np.full((tumor_faces.shape[0], 1), 3), tumor_faces]).astype(np.int32)
    tumor_mesh = pv.PolyData(tumor_verts, tumor_faces)
    # PyVista plot
    plotter = pv.Plotter()
    plotter.add_mesh(brain_mesh, color="lightblue", opacity=0.2, label="Brain")
    plotter.add_mesh(tumor_mesh, color="red", opacity=0.7, label="Tumor")
    plotter.show_axes()
    plotter.add_legend()
    plotter.show()

def main():
    try:
        file_path = select_file()
        print(f"Selected file: {file_path}")
        mri_data = load_mri(file_path)
        tumor_mask = segment_tumor(mri_data)
        render_3d_pyvista(mri_data, tumor_mask)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main() 
