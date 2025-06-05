# MRI 3D Plugin

A self-contained Eliza plugin for 3D MRI brain tumor analysis, segmentation, and AI-powered summarization.

## Features
- Load MRI scans from `.nii.gz` or `.zip` (image stack)
- Normalize and preprocess MRI volumes
- Advanced 3D tumor segmentation
- Visualization of slices with mask overlay
- 3D mesh generation (marching cubes)
- AI-generated medical summary (Gemini API)
- Bundled medical hypotheses

## Usage
Import and call the entry point:
```python
from main import run_mri_3d
results = run_mri_3d('path/to/scan.nii.gz', threshold=0.5, min_size=100, contrast=1.0, brightness=0.0, gemini_api_key='YOUR_KEY')
```

## File Structure
- `main.py`: Core backend logic
- `eliza_plugin.yaml`: Plugin config
- `requirements.txt`: Backend dependencies
- `README.md`: Documentation
- `hypotheses_utf8.txt`: Medical hypotheses (used in summaries)

## Configuration
- All file reads are local to the plugin folder
- No UI code (Streamlit/Flask removed)
- Compatible with Eliza AI plugin standards

## Dependencies
See `requirements.txt`.

## Testing
(Optional) Add tests in `tests/test_main.py`.
