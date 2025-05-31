import streamlit as st
import os
import sys

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Add project directories to Python path
project1_path = os.path.join(project_root, "MRIxAI")
project2_path = os.path.join(project_root, "Genethink AI")
sys.path.extend([project1_path, project2_path])

# Set page configuration
st.set_page_config(
    page_title="𝐍𝐞𝐱𝐨𝐫𝐚 𝐀𝐈",
    page_icon="⚛︎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS for dark, futuristic black and navy blue theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&family=Orbitron:wght@400;500;600;700;800;900&display=swap');

    /* Global Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Define color variables from HTML */
    :root {
        --primary-bg: #0a0a0f;
        --secondary-bg: #0f0f1a;
        --card-bg: rgba(15, 15, 26, 0.8);
        --glass-bg: rgba(20, 25, 45, 0.15);
        --border-color: rgba(64, 224, 255, 0.15);
        --electric-blue: #40e0ff;
        --electric-glow: rgba(64, 224, 255, 0.3);
        --text-primary: #ffffff;
        --text-secondary: rgba(255, 255, 255, 0.7);
        --text-muted: rgba(255, 255, 255, 0.5);
        --shadow-dark: rgba(0, 0, 0, 0.6);
        --shadow-glow: rgba(64, 224, 255, 0.2);
    }

    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
    .css-1d391kg {display: none;}

    /* Main App Container */
    .stApp {
        background: linear-gradient(135deg, 
            var(--primary-bg) 0%, 
            #141428 25%, 
            #1a1a3a 50%, 
            var(--secondary-bg) 75%, 
            #000000 100%);
        background-attachment: fixed;
        min-height: 100vh;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
        overflow-x: hidden;
    }

    /* Main Content Area */
    .main {
        padding: 0;
        margin: 0;
        background: transparent;
    }

    /* Hero Section */
    .hero-section {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 5rem 3rem;
        margin: 2rem auto;
        text-align: center;
        box-shadow: 
            0 8px 32px var(--shadow-dark),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        position: relative;
        max-width: 1400px;
        overflow: hidden;
    }

    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--electric-blue), 
            transparent);
        transform: scaleX(0);
        transition: transform 0.6s ease;
    }

    .hero-section:hover::before {
        transform: scaleX(1);
    }

    /* Main Title - Ultra Professional */
    .main-title {
        font-family: 'Orbitron', 'Space Grotesk', sans-serif;
        font-size: 5rem;
        
        color: #ffffff;
        margin-bottom: 2rem;
        letter-spacing: -3px;
        line-height: 0.9;
        text-shadow: 
            0 0 30px rgba(255, 255, 255, 0.5),
            0 0 60px rgba(255, 255, 255, 0.3),
            0 0 90px rgba(255, 255, 255, 0.1);
        position: relative;
    }

    .main-subtitle {
        font-size: 1.5rem;
        color: var(--text-secondary);
        font-weight: 300;
        line-height: 1.6;
        margin-bottom: 3rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        letter-spacing: 0.5px;
    }

    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2.5rem;
        margin: 5rem auto;
        max-width: 1400px;
        padding: 0 2rem;
    }

    .stat-item {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 32px var(--shadow-dark),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .stat-item::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--electric-blue), 
            transparent);
        transform: scaleX(0);
        transition: transform 0.6s ease;
    }

    .stat-item:hover::after {
        transform: scaleX(1);
    }

    .stat-item:hover {
        transform: translateY(-12px);
        border-color: rgba(64, 224, 255, 0.3);
        box-shadow: 
            0 20px 60px var(--shadow-dark),
            0 0 40px var(--shadow-glow);
    }

    .stat-number {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px var(--shadow-dark);
    }

    .stat-label {
        font-size: 1.1rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Project Cards */
    .projects-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 2rem;
    }

    .project-card {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 4rem 3rem;
        margin-bottom: 3rem;
        transition: all 0.5s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 
            0 8px 32px var(--shadow-dark),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        height: 600px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .project-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, 
            transparent, 
            var(--electric-blue), 
            transparent);
        transform: scaleX(0);
        transition: transform 0.6s ease;
    }

    .project-card:hover::after {
        transform: scaleX(1);
    }

    .project-card:hover {
        transform: translateY(-16px);
        border-color: rgba(64, 224, 255, 0.3);
        box-shadow: 
            0 20px 60px var(--shadow-dark),
            0 0 40px var(--shadow-glow);
    }

    .project-icon {
        font-size: 5rem;
        margin-bottom: 2rem;
        color: var(--electric-blue);
        filter: drop-shadow(0 4px 8px var(--shadow-dark));
        animation: subtleFloat 4s ease-in-out infinite;
    }

    @keyframes subtleFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .project-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 2rem;
        text-align: center;
        letter-spacing: -1px;
        text-shadow: 0 2px 4px var(--shadow-dark);
    }

    .project-description {
        font-size: 1.2rem;
        color: var(--text-secondary);
        line-height: 1.7;
        margin-bottom: 3rem;
        text-align: center;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        flex-grow: 1;
        display: flex;
        align-items: center;
    }

    .features-container {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 3rem;
        width: 100%;
    }

    .feature-tag {
        background: var(--glass-bg);
        color: var(--text-secondary);
        padding: 0.8rem 1.5rem;
        border-radius: 24px;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid var(--border-color);
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }

    .feature-tag:hover {
        transform: translateY(-4px);
        border-color: rgba(64, 224, 255, 0.3);
        background: rgba(64, 224, 255, 0.1);
        color: var(--electric-blue);
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
        padding: 1.5rem 3rem;
        border-radius: 12px;
        background: var(--glass-bg);
        color: var(--text-primary);
        border: 2px solid var(--border-color);
        font-family: 'Space Grotesk', sans-serif;
       font-weight: 400;
        font-size: 1.2rem;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(16px);
    }

    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(64, 224, 255, 0.1), 
            transparent);
        transition: left 0.6s ease;
    }

    .stButton>button:hover::before {
        left: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-4px);
        border-color: rgba(64, 224, 255, 0.3);
        box-shadow: 
            0 20px 40px var(--shadow-dark),
            0 0 20px var(--shadow-glow);
        background: rgba(64, 224, 255, 0.1);
        color: var(--electric-blue);
    }

    /* Footer */
    .footer-container {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        padding: 4rem 2rem;
        text-align: center;
        border-top: 1px solid var(--border-color);
        margin-top: 6rem;
        box-shadow: 
            0 8px 32px var(--shadow-dark),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .footer-title {
        font-size: 1.2rem;
        color: var(--text-primary);
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .footer-subtitle {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.2);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, 
            var(--electric-blue), 
            rgba(64, 224, 255, 0.3));
        border-radius: 3px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, 
            #60f0ff, 
            var(--electric-blue));
    }

    /* Responsive Design */
    @media (max-width: 1200px) {
        .main-title { font-size: 4rem; }
        .project-card { padding: 3rem 2rem; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
    }

    @media (max-width: 768px) {
        .hero-section { padding: 3rem 2rem; }
        .main-title { font-size: 3rem; letter-spacing: -2px; }
        .main-subtitle { font-size: 1.3rem; }
        .project-title { font-size: 2.2rem; }
        .stats-grid { grid-template-columns: 1fr; }
    }

    @media (max-width: 480px) {
        .main-title { font-size: 2.5rem; }
        .project-card { padding: 2rem 1.5rem; }
        .stButton>button { padding: 1.2rem 2rem; font-size: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="main-title">⚛ Nexora AI World </h1>
    <p class="main-subtitle">
       ❝ Next-Gen Neuro-AI for Biomedical Discovery 3D MRI Reconstruction Meets Intelligent Hypothesis Generation ❞
    </p>
</div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("""
<div class="stats-grid">
    <div class="stat-item">
        <span class="stat-number">2</span>
        <div class="stat-label">Active Projects</div>
    </div>
    <div class="stat-item">
        <span class="stat-number">99.9%</span>
        <div class="stat-label">System Uptime</div>
    </div>
    <div class="stat-item">
        <span class="stat-number">847ms</span>
        <div class="stat-label">Processing Speed</div>
    </div>
    <div class="stat-item">
           <span class="stat-number">87.9%</span>
        <div class="stat-label">AI Accuracy</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Projects Section
st.markdown('<div class="projects-container">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="project-card">
        <span class="project-icon">⚛</span>
        <h2 class="project-title">MRIxAI</h2>
        <p class="project-description">
            Advanced Medical Imaging Analysis powered by cutting-edge AI algorithms. 
            Revolutionizing healthcare diagnostics with precision and speed.
        </p>
        <div class="features-container">
            <span class="feature-tag">Medical AI</span>
            <span class="feature-tag">Deep Learning</span>
            <span class="feature-tag">Healthcare</span>
            <span class="feature-tag">Diagnostics</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⚛ Launch MRIxAI", key="mri_button"):
        st.switch_page("pages/1_MRIxAI.py")

with col2:
    st.markdown("""
    <div class="project-card">
        <span class="project-icon">🧬</span>
        <h2 class="project-title">Genethink AI</h2>
        <p class="project-description">
            Next-generation genetic analysis and bioinformatics platform. 
            Unlocking the secrets of DNA with intelligent computational power.
        </p>
        <div class="features-container">
            <span class="feature-tag">Genomics</span>
            <span class="feature-tag">Bioinformatics</span>
            <span class="feature-tag">DNA Analysis</span>
            <span class="feature-tag">Research</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🧬 Launch Genethink AI", key="gene_button"):
        st.switch_page("pages/2_Genethink AI.py")

st.markdown('</div>', unsafe_allow_html=True)

# Footer Section
st.markdown("""
<div class="footer-container">
    <p class="footer-title">╰┈➤ Built with passion for AI innovation | Nexora AI © 2025</p>
    <p class="footer-subtitle">Transforming ideas into intelligent solutions</p>
</div>
""", unsafe_allow_html=True)
