# NexoGPT Plugin

## Overview
The NexoGPT plugin is a specialized medical and biohealth AI assistant that leverages the Groq API to provide accurate information about medical diagnostics, biohealth, genetics, and quantum computing applications in healthcare.

## Features
- Processes individual messages or maintains full chat history
- Connects to Groq Cloud API using meta-llama/llama-4-scout-17b-16e-instruct model
- Handles API errors gracefully with informative error messages
- Configurable response parameters (max tokens, temperature)
- Specialized in medical and biohealth information

## Usage
The plugin exposes a single entry point function:

```python
result = run_nexogpt(prompt, api_key, chat_history=None, max_tokens=200, temperature=0.7)
```

### Parameters
- `prompt`: The user's input message
- `api_key`: Groq API key
- `chat_history`: Optional list of message dictionaries with previous conversation
- `max_tokens`: Maximum number of tokens in the response (default: 200)
- `temperature`: Temperature parameter for response generation (default: 0.7)

### Return Value
The function returns a dictionary with the following structure:

```python
{
    "error": False,
    "content": "The AI assistant's response",
    "usage": {
        "prompt_tokens": 123,
        "completion_tokens": 45,
        "total_tokens": 168
    },
    "model": "meta-llama/llama-4-scout-17b-16e-instruct"
}
```

If an error occurs, it returns:
```python
{
    "error": True,
    "message": "Error message"
}
```

## File Structure
- `main.py`: Contains the core backend logic
- `eliza_plugin.yaml`: Plugin metadata and entry point configuration
- `requirements.txt`: Required dependencies
- `README.md`: Documentation

## Configuration
The plugin requires a Groq API key to be passed as a parameter. No keys are hardcoded in the plugin code.

## Dependencies
- requests: For making HTTP requests to the Groq API
- python-dotenv: For environment variable management (optional, used in original app)

## Testing
To test the plugin, provide a valid Groq API key and verify that it returns a properly formatted response.

## Security Considerations
- API keys are passed as parameters and not stored within the plugin
- The plugin implements proper error handling
- No sensitive data is logged or exposed

## Notes
- This plugin is backend-only and contains no UI code
- It is designed to be modular and self-contained
- The plugin follows best practices for API key management and error handling
