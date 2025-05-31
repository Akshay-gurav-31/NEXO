import streamlit as st
import sys
import os
import importlib.util

# Add PROJECT 2 directory to Python path
project2_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "PROJECT 2")
sys.path.append(project2_path)

# Import the app from the frontend directory
try:
    # Add parent directory to path for imports
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    
    # Add app directory to path
    app_dir = os.path.join(project2_path, "app")
    sys.path.insert(0, app_dir)
    
    # Configure API keys from secrets
    if 'project2' in st.secrets:
        os.environ['GEMINI_API_KEYS'] = ','.join(st.secrets['project2']['gemini_api_keys'])
    
    # Initialize system state in session state if not already done
    if 'system_running' not in st.session_state:
        st.session_state.system_running = False
    if 'hypotheses' not in st.session_state:
        st.session_state.hypotheses = []
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'is_generating' not in st.session_state:
        st.session_state.is_generating = False
    if 'generator' not in st.session_state:
        st.session_state.generator = None

    # Import the app module
    app_path = os.path.join(project2_path, "frontend", "app.py")
    spec = importlib.util.spec_from_file_location("app", app_path)
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
except Exception as e:
    st.error(f"Error loading Genethink AI: {str(e)}")
    st.info("Please make sure all required files exist in the Genethink AI directory.")
finally:
    # Change back to the original directory
    os.chdir(parent_dir) 
