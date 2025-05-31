import streamlit as st
import sys
import os
import importlib.util
import traceback
from typing import Optional

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add MRIxAI directory to Python path
project1_path = os.path.join(project_root, "PROJECT")
sys.path.append(project1_path)

def safe_import_module(module_path: str, module_name: str) -> Optional[object]:
    """Safely import a module with proper error handling."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            st.error(f"Could not find module at {module_path}")
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"Error importing module: {str(e)}")
        st.error(traceback.format_exc())
        return None

def configure_api() -> bool:
    """Configure the API with proper error handling."""
    try:
        if 'GEMINI_API_KEY' in st.secrets:
            api_key = st.secrets['GEMINI_API_KEY']
            os.environ['GEMINI_API_KEY'] = api_key
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            return True
        else:
            st.warning("GEMINI_API_KEY not found in secrets. Some features may be limited.")
            return False
    except Exception as e:
        st.error(f"Error configuring API: {str(e)}")
        st.error(traceback.format_exc())
        return False

# Import the app from the 3d directory
try:
    # Configure API
    if not configure_api():
        st.error("Failed to configure API. Please check your secrets configuration.")
        st.stop()
    
    # Import the app module
    app_path = os.path.join(project1_path, "3d", "app.py")
    app_module = safe_import_module(app_path, "app")
    
    if app_module is None:
        st.error("Failed to load the MRIxAI module.")
        st.stop()
    
except Exception as e:
    st.error(f"Error loading MRIxAI: {str(e)}")
    st.error(traceback.format_exc())
    st.info("Please make sure all required files exist in the MRIxAI directory.")
    st.stop() 
