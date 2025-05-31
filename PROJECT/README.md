# DeepBrainDx AI - Brain MRI Analysis Tool

A Streamlit-based web application for advanced brain MRI analysis and tumor detection using AI.

## Features

- Interactive 3D visualization of brain MRI scans
- Advanced tumor detection and segmentation
- Slice-by-slice analysis with adjustable parameters
- AI-powered medical summary generation using Gemini API
- Support for .nii.gz and .zip file formats
- Real-time tumor statistics and measurements
- Customizable visualization controls

## Prerequisites

- Python 3.x
- Streamlit
- Required Python packages (see requirements.txt)
- Gemini API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Gemini API:
   - Get your API key from Google AI Studio
   - Create a `.streamlit/secrets.toml` file in your project root
   - Add your API key to the secrets file:
     ```toml
     GEMINI_API_KEY="your-api-key-here"
     ```

## Usage

1. Start the Streamlit application:
```bash
streamlit run 3d/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Upload your MRI file (.nii.gz or .zip of slices)

4. Use the sidebar controls to adjust detection parameters:
   - Detection Threshold
   - Minimum Tumor Size
   - Visualization settings

5. Explore the different tabs:
   - 3D Visualization
   - Slice Analysis
   - Tumor Detection Details
   - AI Doctor Summary

## Project Structure

```
├── 3d/
│   ├── app.py           # Main Streamlit application
│   ├── templates/       # Template files
│   └── .streamlit/      # Streamlit configuration
├── .streamlit/
│   └── secrets.toml     # API keys and secrets (not tracked in git)
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## Environment Variables

The following environment variables need to be set:

- `GEMINI_API_KEY`: Your Google Gemini API key

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Security

- Never commit your API keys or secrets
- Keep your `.streamlit/secrets.toml` file secure and out of version control
- Use environment variables for sensitive data in production

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/projectname](https://github.com/yourusername/projectname) 