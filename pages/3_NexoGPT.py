import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(page_title="NexoGPT-1.2", layout="wide")

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Welcome to NexoGPT-1.2! I'm here to help with your medical and biohealth questions. How can I assist you today?"
    })

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

# Back to Home button (relative URL for deployment compatibility)
st.markdown("""
    <a href="/" class="back-button" style="
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
    # Header with Clear Chat icon
    col1, col2 = st.columns([9, 1])
    with col1:
        st.markdown('<h2 style="color: #d4af37;">🤖 NexoGPT-1.2 - Medical & Biohealth Assistant</h2>', unsafe_allow_html=True)
    with col2:
        if st.button("🗑️", key="clear_chat", help="Clear chat"):
            st.session_state.messages = [{"role": "assistant", "content": "Welcome to NexoGPT-1.2! I'm here to help with your medical and biohealth questions. How can I assist you today?"}]
            st.experimental_rerun()

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f'<div class="message-bubble {message["role"]}-message">{message["content"]}</div>', unsafe_allow_html=True)

    # User input
    if prompt := st.chat_input("Ask about medical or biohealth topics..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(f'<div class="message-bubble user-message">{prompt}</div>', unsafe_allow_html=True)

        # Get assistant response
        with st.spinner("Processing..."):
            response = process_message(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(f'<div class="message-bubble assistant-message">{response}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Function to call Groq Cloud API
def process_message(prompt):
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    if not GROQ_API_KEY:
        return "Please set up your Groq API key in the environment variables."

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
            json=data
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        elif response.status_code == 429:
            return "Error: Rate limit exceeded. Please try again later."
        elif response.status_code == 401:
            return "Error: Invalid API key. Please check your Groq API key."
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error processing request: {str(e)}"

# Run the app
if __name__ == "__main__":
    chat_interface()
