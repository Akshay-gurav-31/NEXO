import streamlit as st
import requests
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure page
try:
    st.set_page_config(
        page_title="NX-News-BIO",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception as e:
    st.error(f"Error setting page configuration: {str(e)}")
    logger.error(f"Page config error: {str(e)}")
    st.stop()

# Initialize session state
if 'news_data' not in st.session_state:
    st.session_state.news_data = []

# Custom CSS for styling
st.markdown("""
<style>
    .news-container {
        background: rgba(15, 15, 31, 0.8);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        backdrop-filter: blur(10px);
    }
    .news-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    .news-card:hover {
        transform: translateY(-5px);
    }
    .news-title {
        color: #d4af37;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    .news-source {
        color: #4a2c7a;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    .news-date {
        color: #ffffff;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .news-content {
        color: #ffffff;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .read-more {
        color: #d4af37;
        text-decoration: none;
        font-weight: bold;
    }
    .read-more:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Back to Home button
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

# Page title
st.markdown("""
<div class="news-container">
    <h2 style="color: #d4af37; text-align: center; margin-bottom: 2rem;">
        📰 NX-News-BIO - Latest Medical & Biohealth News
    </h2>
</div>
""", unsafe_allow_html=True)

# Function to fetch news
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_news():
    try:
        # Validate API key
        api_key = '220cf0fc01744c609a262a7409b31aea'
        if not api_key:
            error_msg = "News API key is not configured."
            logger.error(error_msg)
            return None, error_msg

        # Query for medical and biohealth news
        params = {
            'q': 'healthcare OR medical OR science OR research OR genetics OR medicine OR vaccine OR treatment',
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': api_key,
            'pageSize': 100
        }

        response = requests.get(
            'https://newsapi.org/v2/everything',
            params=params,
            timeout=30  # Added timeout for robustness
        )

        response.raise_for_status()  # Raises HTTPError for bad status codes

        data = response.json()

        # Display API response in a compact format
        st.markdown(f"""
        <div style="background: rgba(15, 15, 31, 0.8); padding: 1rem; border-radius: 10px;">
            <h3 style="color: #d4af37; margin-bottom: 0.5rem;">Response</h3>
            <div style="color: white;">
                <pre style="margin: 0; font-size: 0.9rem;">
                    Status: {response.status_code}
                    Message: {data.get('message', 'Success')}
                    Articles: {len(data.get('articles', []))}
                </pre>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if 'articles' in data and len(data['articles']) > 0:
            st.session_state.news_data = data['articles']
            return data, None
        else:
            error_msg = "No news articles found."
            st.warning(error_msg)
            st.write(data)
            logger.warning(f"No articles in response: {data}")
            return None, error_msg

    except requests.exceptions.HTTPError as http_err:
        error_msg = f"HTTP error: {str(http_err)}"
        if response.status_code == 401:
            error_msg = "Error: Invalid News API key."
        elif response.status_code == 429:
            error_msg = "Error: Rate limit exceeded. Please try again later."
        st.error(error_msg)
        logger.error(error_msg)
        return None, error_msg
    except requests.exceptions.Timeout:
        error_msg = "Error: Request timed out. Please try again."
        st.error(error_msg)
        logger.error(error_msg)
        return None, error_msg
    except requests.exceptions.RequestException as req_err:
        error_msg = f"Error fetching news: {str(req_err)}"
        st.error(error_msg)
        logger.error(error_msg)
        return None, error_msg
    except ValueError as val_err:
        error_msg = f"Error parsing response: {str(val_err)}"
        st.error(error_msg)
        logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        st.error(error_msg)
        logger.error(error_msg)
        return None, error_msg
    
    
    
    

# Fetch and display news
try:
    news_data, error = fetch_news()
    if error:
        st.error(f"Failed to fetch news: {error}")
    elif news_data and news_data.get('articles'):
        st.session_state.news_data = news_data['articles']

        # Display news in columns
        col1, col2 = st.columns(2)

        for i, article in enumerate(st.session_state.news_data):
            try:
                with col1 if i % 2 == 0 else col2:
                    title = article.get('title', 'No Title')
                    source = article.get('source', {}).get('name', 'Unknown Source')
                    published_at = article.get('publishedAt', datetime.now().isoformat())
                    content = article.get('content', 'No content available') or 'No content available'
                    url = article.get('url', '#')

                    st.markdown(f"""
                    <div class="news-card">
                        <h3 class="news-title">{title}</h3>
                        <div class="news-source">{source}</div>
                        <div class="news-date">{datetime.fromisoformat(published_at).strftime('%B %d, %Y')}</div>
                        <div class="news-content">{content}</div>
                        <a href="{url}" target="_blank" class="read-more">Read More →</a>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.warning(f"Error displaying article: {str(e)}")
                logger.warning(f"Article display error: {str(e)}")
except Exception as e:
    st.error(f"Error in news display: {str(e)}")
    logger.error(f"News display error: {str(e)}")
