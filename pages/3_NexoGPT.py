import streamlit as st
import requests
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    st.error(f"Failed to load environment variables: {str(e)}")
    logger.error(f"Environment variable loading error: {str(e)}")
    st.stop()

# Configure page
try:
    st.set_page_config(
        page_title="NexoGPT-1.2",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception as e:
    st.error(f"Error setting page configuration: {str(e)}")
    logger.error(f"Page config error: {str(e)}")
    st.stop()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Welcome to NexoGPT-1.2! I'm here to help with your medical and biohealth questions. How can I assist you today?"
        }
    ]

# Custom CSS for styling
st.markdown("""
<style>
    .chat-container {
        background: rgba(15, 15, 31, 0.8);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        backdrop-filter: blur(10px);
    }
    .message-bubble {
        padding: 1rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    .user-message {
        background: #4a2c7a;
        margin-left: auto;
        color: white;
    }
    .assistant-message {
        background: #1a1a3a;
        margin-right: auto;
        color: white;
    }
    .clear-button {
        background-color: transparent;
        border: none;
        color: #d4af37;
        cursor: pointer;
        font-size: 1.2rem;
        float: right;
        margin-top: -30px;
        margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Back to Home button with absolute URL
st.markdown("""
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

# Chat interface
def chat_interface():
    try:
        # Header with Clear Chat icon
        col1, col2 = st.columns([9, 1])
        with col1:
            st.markdown('<h2 style="color: #d4af37;">🤖 NexoGPT-1.2 - Medical & Biohealth Assistant</h2>', unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key="clear_chat", help="Clear chat"):
                try:
                    st.session_state.messages = [
                        {
                            "role": "assistant",
                            "content": "Welcome to NexoGPT-1.2! I'm here to help with your medical and biohealth questions. How can I assist you today?"
                        }
                    ]
                    st.rerun()  # Replaced st.experimental_rerun with st.rerun
                except Exception as e:
                    st.error(f"Failed to clear chat: {str(e)}")
                    logger.error(f"Chat clear error: {str(e)}")

        # Chat container
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)

        # Display chat history
        for message in st.session_state.messages:
            try:
                with st.chat_message(message["role"]):
                    st.markdown(f'<div class="message-bubble {message["role"]}-message">{message["content"]}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Error displaying message: {str(e)}")
                logger.warning(f"Message display error: {str(e)}")

        # User input
        if prompt := st.chat_input("Ask about medical or biohealth topics..."):
            try:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(f'<div class="message-bubble user-message">{prompt}</div>', unsafe_allow_html=True)

                # Get assistant response
                with st.spinner("Processing..."):
                    response = process_message(prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(f'<div class="message-bubble assistant-message">{response}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error processing user input: {str(e)}")
                logger.error(f"User input processing error: {str(e)}")

        st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error in chat interface: {str(e)}")
        logger.error(f"Chat interface error: {str(e)}")

# Function to call Groq Cloud API
def process_message(prompt):
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    if not GROQ_API_KEY:
        error_msg = "Please set up your Groq API key in the environment variables."
        logger.error(error_msg)
        return error_msg

    system_prompt = """
    You are NexoGPT-1.2, a specialized medical and biohealth AI assistant. 
    Focus on providing accurate information about medical diagnostics, 
    biohealth, genetics, and quantum computing applications in healthcare.
    """

    try:
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }

        data = {
            'model': 'meta-llama/llama-4-scout-17b-16e-instruct',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 200,
            'temperature': 0.7
        }

        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30  # Added timeout for robustness
        )

        response.raise_for_status()  # Raises HTTPError for bad status codes

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            error_msg = f"Unexpected status code: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return error_msg

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 429:
            error_msg = "Error: Rate limit exceeded. Please try again later."
        elif response.status_code == 401:
            error_msg = "Error: Invalid API key. Please check your Groq API key."
        else:
            error_msg = f"HTTP error: {str(http_err)}"
        logger.error(error_msg)
        return error_msg
    except requests.exceptions.Timeout:
        error_msg = "Error: Request timed out. Please try again."
        logger.error(error_msg)
        return error_msg
    except requests.exceptions.RequestException as req_err:
        error_msg = f"Error processing request: {str(req_err)}"
        logger.error(error_msg)
        return error_msg
    except ValueError as val_err:
        error_msg = f"Error parsing response: {str(val_err)}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return error_msg

# Run the app
if __name__ == "__main__":
    try:
        chat_interface()
    except Exception as e:
        st.error(f"Application failed to start: {str(e)}")
        logger.error(f"Application error: {str(e)}")
