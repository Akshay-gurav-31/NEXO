# Eliza Plugins Guide

## Overview

This guide provides instructions for running and testing the Eliza AI-compatible plugins that have been extracted from the original Python project. Each plugin is designed to be modular, self-contained, and focused on backend logic only.

## Plugin Directory Structure

Each plugin follows a standardized structure:

```
eliza_plugins/
├── plugin_name/
│   ├── README.md           # Documentation
│   ├── eliza_plugin.yaml   # Plugin metadata and entry point
│   ├── main.py             # Core backend logic
│   ├── requirements.txt    # Dependencies
│   └── [additional files]  # Plugin-specific resources
```

## Available Plugins

### 1. MRI 3D Plugin (`mri_3d_plugin`)

**Purpose:** 3D MRI brain tumor analysis

**Entry Point:** `run_mri_3d(file_path, threshold=0.5, min_size=100, gemini_api_key=None)`

**Dependencies:**
- numpy
- nibabel
- scikit-image
- scipy
- opencv-python-headless
- plotly
- google-generativeai (optional, for AI summary)

### 2. Genethink AI Plugin (`genethink_ai_plugin`)

**Purpose:** Generate scientific hypotheses using Gemini AI

**Entry Point:** `run_genethink_ai(api_keys)`

**Dependencies:**
- requests
- python-dateutil
- uuid

### 3. NexoGPT Plugin (`nexogpt_plugin`)

**Purpose:** Medical and biohealth AI assistant using Groq API

**Entry Point:** `run_nexogpt(prompt, api_key, chat_history=None, max_tokens=200, temperature=0.7)`

**Dependencies:**
- requests
- python-dotenv

### 4. NewsNX Plugin (`newsnx_plugin`)

**Purpose:** Medical and biohealth news aggregator using NewsAPI

**Entry Point:** `run_newsnx(api_key, query=None, language='en', page_size=20, sort_by='publishedAt', category_filter=None, search_term=None)`

**Dependencies:**
- requests

## Installation

1. Ensure you have Python 3.8+ installed
2. Install plugin dependencies:

```bash
# For a specific plugin
cd eliza_plugins/plugin_name
pip install -r requirements.txt

# For all plugins
for plugin in eliza_plugins/*; do
    if [ -f "$plugin/requirements.txt" ]; then
        pip install -r "$plugin/requirements.txt"
    fi
done
```

## Running the Plugins

### Method 1: Direct Import

You can import and use each plugin directly in your Python code:

```python
import sys
sys.path.append('/path/to/project')

# Example for MRI 3D Plugin
from eliza_plugins.mri_3d_plugin.main import run_mri_3d

result = run_mri_3d(
    file_path='path/to/mri.nii.gz',
    threshold=0.5,
    min_size=100,
    gemini_api_key='your_api_key'
)

print(result)
```

### Method 2: Using Test Scripts

Each plugin has a corresponding test script that demonstrates its usage:

```bash
# Run a specific test
python test_mri_3d_plugin.py
python test_genethink_ai_plugin.py
python test_nexogpt_plugin.py
python test_newsnx_plugin.py

# Run all tests
python run_all_tests.py
```

### Method 3: Integration with Eliza AI Framework

The plugins are designed to be discovered and loaded by the Eliza AI framework:

1. Place the plugin folders in the Eliza plugins directory
2. The framework will automatically discover plugins through the `eliza_plugin.yaml` files
3. The framework will call the entry point function specified in each YAML file

## API Key Management

For security, it's recommended to:

1. Store API keys in environment variables
2. Pass them as parameters to the plugin functions
3. Never hardcode them in your scripts

Example:

```python
import os
from eliza_plugins.nexogpt_plugin.main import run_nexogpt

# Get API key from environment variable
api_key = os.environ.get("GROQ_API_KEY")

# Run plugin
result = run_nexogpt("Hello", api_key)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the project root is in your Python path

   ```python
   import sys
   import os
   sys.path.append(os.path.dirname(os.path.abspath(__file__)))
   ```

2. **Missing Dependencies**: Check that all requirements are installed

   ```bash
   pip install -r eliza_plugins/plugin_name/requirements.txt
   ```

3. **API Key Errors**: Verify that valid API keys are provided

4. **File Not Found**: Check that file paths are correct and accessible

## Development and Extension

To create a new plugin:

1. Create a new directory in `eliza_plugins/`
2. Create the required files: `main.py`, `eliza_plugin.yaml`, `requirements.txt`, `README.md`
3. Implement the entry point function in `main.py`
4. Specify the entry point in `eliza_plugin.yaml`
5. List dependencies in `requirements.txt`
6. Document the plugin in `README.md`

## Contact and Support

For questions or issues, please contact the project maintainers.
