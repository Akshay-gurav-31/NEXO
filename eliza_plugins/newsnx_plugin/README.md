# NewsNX Plugin

## Overview
The NewsNX plugin is a specialized medical and biohealth news aggregator that leverages the NewsAPI to fetch, filter, and process relevant healthcare news articles.

## Features
- Fetches medical and biohealth news from NewsAPI
- Processes and standardizes article format
- Provides filtering by category or search term
- Handles API errors gracefully with informative error messages
- Configurable query parameters (language, page size, sorting)

## Usage
The plugin exposes a single entry point function:

```python
result = run_newsnx(api_key, query=None, language='en', page_size=20, 
                   sort_by='publishedAt', category_filter=None, search_term=None)
```

### Parameters
- `api_key`: NewsAPI key (required)
- `query`: Search query (default: medical and biohealth related terms)
- `language`: News language (default: 'en' for English)
- `page_size`: Number of articles to return (default: 20)
- `sort_by`: Sorting order (default: 'publishedAt')
- `category_filter`: Optional category to filter results by
- `search_term`: Optional search term to filter results by

### Return Value
The function returns a dictionary with the following structure:

```python
{
    "error": False,
    "articles": [
        {
            "title": "Article Title",
            "source": "Source Name",
            "author": "Author Name",
            "published_at": "2025-06-04 12:30:45",
            "description": "Article description",
            "content": "Article content",
            "url": "https://article-url.com",
            "image_url": "https://image-url.com"
        },
        # More articles...
    ],
    "total_results": 100,
    "status": "ok",
    "filtered_count": 20
}
```

If an error occurs, it returns:
```python
{
    "error": True,
    "message": "Error message",
    # Additional error details if available
}
```

## File Structure
- `main.py`: Contains the core backend logic
- `eliza_plugin.yaml`: Plugin metadata and entry point configuration
- `requirements.txt`: Required dependencies
- `README.md`: Documentation

## Configuration
The plugin requires a NewsAPI key to be passed as a parameter. No keys are hardcoded in the plugin code.

## Dependencies
- requests: For making HTTP requests to the NewsAPI

## Testing
To test the plugin, provide a valid NewsAPI key and verify that it returns properly formatted news articles.

### Example Test
```python
from eliza_plugins.newsnx_plugin.main import run_newsnx

# Replace with your actual API key
api_key = "your_newsapi_key"

# Basic test
result = run_newsnx(api_key, page_size=5)
print(f"Fetched {len(result.get('articles', []))} articles")

# Test with category filter
filtered_result = run_newsnx(api_key, page_size=5, category_filter="vaccine")
print(f"Filtered to {len(filtered_result.get('articles', []))} vaccine-related articles")
```

## Security Considerations
- API keys are passed as parameters and not stored within the plugin
- The plugin implements proper error handling
- No sensitive data is logged or exposed

## Notes
- This plugin is backend-only and contains no UI code
- It is designed to be modular and self-contained
- The plugin follows best practices for API key management and error handling
- The default query focuses on medical and biohealth topics, but can be customized
