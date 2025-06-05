# Genethink AI Plugin

## Overview
The Genethink AI plugin generates unique scientific hypotheses using the Gemini AI model. It features a resilient API client that manages multiple API keys with automatic rotation, cooldown periods, and failure handling to ensure reliable operation.

## Features
- Generates unique scientific hypotheses with statements, background, expected outcomes, and implications
- Resilient API management with automatic key rotation
- Handles API rate limits and errors gracefully
- Prevents duplicate hypothesis generation
- Provides API usage statistics

## Usage
The plugin exposes a single entry point function:

```python
result = run_genethink_ai(api_keys)
```

### Parameters
- `api_keys`: List of Gemini API keys to use for hypothesis generation

### Return Value
The function returns a dictionary with the following structure:

```python
{
    "id": "unique-uuid",
    "timestamp": "2025-06-04T01:30:00.000000",
    "statement": "The scientific hypothesis statement",
    "background": "Background information and context",
    "expected_outcomes": ["Expected outcome 1", "Expected outcome 2", ...],
    "implications": ["Implication 1", "Implication 2", ...],
    "api_stats": {
        "total_keys": 5,
        "available_keys": 4,
        "unavailable_keys": 1,
        "key_details": {...}
    }
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
The plugin requires Gemini API keys to be passed as a parameter. No keys are hardcoded in the plugin code.

## Dependencies
- requests: For making HTTP requests to the Gemini API
- python-dateutil: For date/time handling
- uuid: For generating unique identifiers

## Testing
To test the plugin, provide valid Gemini API keys and verify that it returns a properly formatted hypothesis.

## Security Considerations
- API keys are passed as parameters and not stored within the plugin
- The plugin implements proper error handling and rate limiting
- No sensitive data is logged or exposed

## Notes
- This plugin is backend-only and contains no UI code
- It is designed to be modular and self-contained
- The plugin follows best practices for API key management and error handling
