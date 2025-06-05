import requests
from typing import Dict, Any, Optional, List

def process_message(prompt: str, api_key: str) -> str:
    """
    Process a user message and get a response from the Groq API.
    
    Args:
        prompt: The user's input message
        api_key: Groq API key
        
    Returns:
        The AI assistant's response as a string
    """
    if not api_key:
        return "Please provide a valid Groq API key."

    system_prompt = """
    You are NexoGPT-1.2, a specialized medical and biohealth AI assistant. 
    Focus on providing accurate information about medical diagnostics, 
    biohealth, genetics, and quantum computing applications in healthcare.
    """

    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
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


def chat_completion(messages: List[Dict[str, str]], api_key: str, 
                    max_tokens: int = 200, temperature: float = 0.7) -> Dict[str, Any]:
    """
    Get a chat completion from the Groq API with full message history.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        api_key: Groq API key
        max_tokens: Maximum number of tokens in the response
        temperature: Temperature parameter for response generation
        
    Returns:
        Dictionary containing the response and status information
    """
    if not api_key:
        return {"error": True, "message": "Please provide a valid Groq API key."}

    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Add system message if not present
        if not any(msg.get('role') == 'system' for msg in messages):
            system_message = {
                'role': 'system',
                'content': """
                You are NexoGPT-1.2, a specialized medical and biohealth AI assistant. 
                Focus on providing accurate information about medical diagnostics, 
                biohealth, genetics, and quantum computing applications in healthcare.
                """
            }
            messages = [system_message] + messages

        data = {
            'model': 'meta-llama/llama-4-scout-17b-16e-instruct',
            'messages': messages,
            'max_tokens': max_tokens,
            'temperature': temperature
        }

        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            response_data = response.json()
            return {
                "error": False,
                "content": response_data['choices'][0]['message']['content'].strip(),
                "usage": response_data.get('usage', {}),
                "model": response_data.get('model', 'meta-llama/llama-4-scout-17b-16e-instruct')
            }
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": f"API Error: {response.text}"
            }

    except Exception as e:
        return {
            "error": True,
            "message": f"Error processing request: {str(e)}"
        }


def run_nexogpt(prompt: str, api_key: str, 
               chat_history: Optional[List[Dict[str, str]]] = None,
               max_tokens: int = 200, 
               temperature: float = 0.7) -> Dict[str, Any]:
    """
    Main entry point for the NexoGPT plugin.
    
    This function processes a user prompt and returns a response from the Groq API.
    It can either process a single message or handle a full chat history.
    
    Args:
        prompt: The user's input message (used if chat_history is None)
        api_key: Groq API key
        chat_history: Optional list of message dictionaries with previous conversation
        max_tokens: Maximum number of tokens in the response
        temperature: Temperature parameter for response generation
        
    Returns:
        Dictionary containing the response and status information
    """
    try:
        if chat_history:
            # Add the new user prompt to the chat history
            chat_history.append({"role": "user", "content": prompt})
            result = chat_completion(chat_history, api_key, max_tokens, temperature)
        else:
            # Process a single message
            response_text = process_message(prompt, api_key)
            result = {
                "error": "Error" in response_text,
                "content": response_text
            }
            
        return result
    
    except Exception as e:
        return {
            "error": True,
            "message": f"Error in NexoGPT plugin: {str(e)}"
        }
