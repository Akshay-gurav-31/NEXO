import streamlit as st
import requests
from datetime import datetime, timedelta

# Configure page
st.set_page_config(page_title="NX-News-BIO", layout="wide")

# Initialize session state
if 'news_data' not in st.session_state:
    st.session_state.news_data = []

# Function to fetch news
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_news():
    try:
        # Query for medical and biohealth news
        params = {
            'q': 'healthcare OR medical OR science OR research OR genetics OR medicine OR vaccine OR treatment',
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': '220cf0fc01744c609a262a7409b31aea',
            'pageSize': 100
        }
        
        response = requests.get(
            'https://newsapi.org/v2/everything',
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if 'articles' in data and len(data['articles']) > 0:
                st.session_state.news_data = data['articles']
                
                # Display news in a clean format
                st.markdown("""
                <style>
                    .news-container {
                        background: rgba(15, 15, 31, 0.8);
                        border-radius: 20px;
                        padding: 1rem;
                        margin: 1rem;
                        backdrop-filter: blur(10px);
                    }
                    .news-card {
                        background: rgba(255, 255, 255, 0.1);
                        border-radius: 15px;
                        padding: 1rem;
                        margin: 1rem 0;
                        transition: transform 0.2s;
                    }
                    .news-card:hover {
                        transform: translateY(-5px);
                    }
                    .news-title {
                        color: #d4af37;
                        font-size: 1.2rem;
                        margin-bottom: 0.5rem;
                    }
                    .news-source {
                        color: #4a2c7a;
                        font-size: 0.9rem;
                        margin-bottom: 0.5rem;
                    }
                    .news-date {
                        color: #ffffff;
                        font-size: 0.8rem;
                        margin-bottom: 0.5rem;
                    }
                    .news-content {
                        color: #ffffff;
                        font-size: 0.9rem;
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
                
            
                # Display articles in columns
                col1, col2 = st.columns(2)
                
                for i, article in enumerate(st.session_state.news_data):
                    with col1 if i % 2 == 0 else col2:
                        st.markdown(f"""
                        <div class="news-card">
                            <h3 class="news-title">{article.get('title', 'No Title')}</h3>
                            <div class="news-source">{article.get('source', {}).get('name', 'Unknown Source')}</div>
                            <div class="news-date">{article.get('publishedAt', datetime.now().isoformat())[:10]}</div>
                            <div class="news-content">{article.get('description', 'No description available')}</div>
                            <a href="{article.get('url', '#')}" target="_blank" class="read-more">Read More →</a>
                        </div>
                        """, unsafe_allow_html=True)
                
                return data
            else:
                st.warning("No news articles found. Full response:")
                st.write(data)
                return None
        
        if response.status_code == 200:
            data = response.json()
            
            # Display API response in a compact format
            st.markdown(f"""
            <div style="background: rgba(15, 15, 31, 0.8); padding: 1rem; border-radius: 10px;">
                <h3 style="color: #d4af37; margin-bottom: 0.5rem;">API Response</h3>
                <div style="color: white;">
                    <pre style="margin: 0; font-size: 0.9rem;">
                        Status: {response.status_code}
                        Message: {data.get('message', 'No message')}
                        Articles: {len(data.get('articles', []))}
                    </pre>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if 'articles' in data and len(data['articles']) > 0:
                return data
            else:
                st.warning("No news articles found. Check the API response above.")
                return None
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return None

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

# Page title
st.markdown("""
<div class="news-container">
    <h2 style="color: #d4af37; text-align: center; margin-bottom: 2rem;">
        📰 NX-News-BIO - Latest Medical & Biohealth News
    </h2>
</div>
""", unsafe_allow_html=True)

# Fetch news
news_data = fetch_news()

if news_data and news_data.get('articles'):
    st.session_state.news_data = news_data['articles']
    
    # Display news in columns
    col1, col2 = st.columns(2)
    
    for i, article in enumerate(st.session_state.news_data):
        with col1 if i % 2 == 0 else col2:
            title = article.get('title', 'No Title')
            source = article.get('source', {}).get('name', 'Unknown Source')
            published_at = article.get('published_at', datetime.now().isoformat())
            content = article.get('content', 'No content available')
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

else:
    st.error("Failed to fetch news. Please try again later.")
