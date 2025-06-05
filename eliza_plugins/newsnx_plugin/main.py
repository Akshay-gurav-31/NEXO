import requests
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

def fetch_medical_news(api_key: str, query: str = None, language: str = 'en', 
                       page_size: int = 20, sort_by: str = 'publishedAt') -> Dict[str, Any]:
    """
    Fetch medical and biohealth news from NewsAPI.
    
    Args:
        api_key: NewsAPI key
        query: Search query (default: medical and biohealth related terms)
        language: News language (default: 'en' for English)
        page_size: Number of articles to return (default: 20)
        sort_by: Sorting order (default: 'publishedAt')
        
    Returns:
        Dictionary containing news articles and metadata
    """
    if not api_key:
        return {
            "error": True,
            "message": "Please provide a valid NewsAPI key."
        }
    
    # Default query for medical and biohealth news if none provided
    if not query:
        query = 'healthcare OR medical OR science OR research OR genetics OR medicine OR vaccine OR treatment'
    
    try:
        # Set up query parameters
        params = {
            'q': query,
            'sortBy': sort_by,
            'language': language,
            'apiKey': api_key,
            'pageSize': page_size
        }
        
        # Make API request
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Process articles to standardize format
            if 'articles' in data and len(data['articles']) > 0:
                processed_articles = []
                
                for article in data['articles']:
                    # Format date
                    published_date = article.get('publishedAt', datetime.now().isoformat())
                    if isinstance(published_date, str):
                        try:
                            # Convert to datetime object for consistent formatting
                            date_obj = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
                            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            formatted_date = published_date
                    else:
                        formatted_date = published_date
                    
                    # Create standardized article object
                    processed_article = {
                        'title': article.get('title', 'No Title'),
                        'source': article.get('source', {}).get('name', 'Unknown Source'),
                        'author': article.get('author', 'Unknown Author'),
                        'published_at': formatted_date,
                        'description': article.get('description', 'No description available'),
                        'content': article.get('content', 'No content available'),
                        'url': article.get('url', '#'),
                        'image_url': article.get('urlToImage', None)
                    }
                    
                    processed_articles.append(processed_article)
                
                return {
                    "error": False,
                    "articles": processed_articles,
                    "total_results": data.get('totalResults', len(processed_articles)),
                    "status": data.get('status', 'ok')
                }
            else:
                return {
                    "error": True,
                    "message": "No news articles found.",
                    "raw_response": data
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
            "message": f"Error fetching news: {str(e)}"
        }

def filter_articles_by_category(articles: List[Dict[str, Any]], category: str) -> List[Dict[str, Any]]:
    """
    Filter articles by category based on keywords in title or description.
    
    Args:
        articles: List of article dictionaries
        category: Category to filter by (e.g., 'research', 'treatment', 'vaccine')
        
    Returns:
        Filtered list of articles
    """
    if not articles or not category:
        return articles
    
    category = category.lower()
    filtered_articles = []
    
    for article in articles:
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        content = article.get('content', '').lower()
        
        if (category in title) or (category in description) or (category in content):
            filtered_articles.append(article)
    
    return filtered_articles

def search_articles(articles: List[Dict[str, Any]], search_term: str) -> List[Dict[str, Any]]:
    """
    Search articles for a specific term in title, description, or content.
    
    Args:
        articles: List of article dictionaries
        search_term: Term to search for
        
    Returns:
        Filtered list of articles containing the search term
    """
    if not articles or not search_term:
        return articles
    
    search_term = search_term.lower()
    search_results = []
    
    for article in articles:
        title = article.get('title', '').lower()
        description = article.get('description', '').lower()
        content = article.get('content', '').lower()
        
        if (search_term in title) or (search_term in description) or (search_term in content):
            search_results.append(article)
    
    return search_results

def run_newsnx(api_key: str, query: str = None, language: str = 'en', 
               page_size: int = 20, sort_by: str = 'publishedAt',
               category_filter: str = None, search_term: str = None) -> Dict[str, Any]:
    """
    Main entry point for the NewsNX plugin.
    
    This function fetches medical and biohealth news and optionally filters the results.
    
    Args:
        api_key: NewsAPI key
        query: Search query (default: medical and biohealth related terms)
        language: News language (default: 'en' for English)
        page_size: Number of articles to return (default: 20)
        sort_by: Sorting order (default: 'publishedAt')
        category_filter: Optional category to filter results by
        search_term: Optional search term to filter results by
        
    Returns:
        Dictionary containing news articles and metadata
    """
    try:
        # Fetch news articles
        result = fetch_medical_news(api_key, query, language, page_size, sort_by)
        
        # Check if there was an error
        if result.get('error', False):
            return result
        
        articles = result.get('articles', [])
        
        # Apply category filter if specified
        if category_filter and articles:
            articles = filter_articles_by_category(articles, category_filter)
        
        # Apply search filter if specified
        if search_term and articles:
            articles = search_articles(articles, search_term)
        
        # Update the result with filtered articles
        result['articles'] = articles
        result['filtered_count'] = len(articles)
        
        return result
    
    except Exception as e:
        return {
            "error": True,
            "message": f"Error in NewsNX plugin: {str(e)}"
        }
