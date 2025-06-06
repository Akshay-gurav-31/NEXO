import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure page
try:
    st.set_page_config(
        page_title="About Nexora AI",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception as e:
    st.error(f"Error setting page configuration: {str(e)}")
    logger.error(f"Page config error: {str(e)}")
    st.stop()

# Custom CSS for navy blue theme
st.markdown("""
<style>
    .container {
        background: rgba(15, 15, 31, 0.8);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        backdrop-filter: blur(10px);
    }
    .title {
        color: #D4AF37;
        text-align: center;
        margin-bottom: 1.5rem;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .subheader {
        color: #D4AF37;
        margin: 1.5rem 0 1rem;
        font-size: 1.8rem;
        font-weight: 600;
    }
    .content {
        color: #FFFFFF;
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    .project-card {
        background: rgba(0, 31, 63, 0.9); /* Navy blue */
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    .project-card:hover {
        transform: translateY(-5px);
    }
    .project-title {
        color: #D4AF37;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    .project-content {
        color: #FFFFFF;
        font-size: 1rem;
        line-height: 1.5;
    }
    .mission-box {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: #FFFFFF;
        font-size: 1.1rem;
        text-align: center;
        font-style: italic;
    }
    .back-button {
        display: inline-block;
        padding: 8px 16px;
        background-color: #001F3F; /* Navy blue */
        color: #FFFFFF;
        text-decoration: none;
        border-radius: 5px;
        font-weight: 600;
        margin-bottom: 1rem;
        transition: background-color 0.2s;
    }
    .back-button:hover {
        background-color: #003087; /* Slightly lighter navy blue */
    }
    hr {
        border-color: #4A2C7A;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Back to Home button
st.markdown("""
    <a href="https://nexo-xadw.onrender.com/" class="back-button">Back to Home</a>
""", unsafe_allow_html=True)

# Page content
try:
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">About Nexora AI</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div class="content">
        <strong>Nexora AI</strong> stands as a pioneer in the fusion of quantum computing and artificial intelligence, driving transformative advancements in healthcare and genomics. Our mission is to address critical challenges in medical diagnostics and gene editing by delivering unparalleled precision, speed, and intelligence through quantum-enhanced technologies.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<h2 class="subheader">The Problem We Solve</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="content">
        The healthcare industry faces significant hurdles in achieving rapid, accurate, and scalable solutions for complex medical diagnostics and personalized treatments. Traditional methods often lack the computational power to process vast datasets, such as genomic sequences or high-resolution medical imaging, with the speed and precision required for real-time applications. Nexora AI bridges this gap by leveraging quantum-enhanced neural networks to revolutionize medical imaging, gene editing, and clinical decision-making.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<h2 class="subheader">Our Solutions</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="content">
        Nexora AI tackles these challenges through a suite of innovative projects, each designed to push the boundaries of healthcare technology:
    </div>
    """, unsafe_allow_html=True)

    # Project Cards
    st.markdown("""
    <div class="project-card">
        <h3 class="project-title">MRIxAI</h3>
        <div class="project-content">
            MRIxAI harnesses quantum-enhanced neural networks to redefine medical imaging and anomaly detection. It provides AI-generated medical summaries, including detailed interpretations of MRI brain analysis, identification of lesions (e.g., tumors), their volume, and confidence levels. The platform offers actionable recommendations, such as repeating MRI scans, expert image review, clinical correlation, or advanced imaging. Users can explore MRI data in 3D, view slices, and access comprehensive summaries, enabling faster and more accurate diagnostics.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="project-card">
        <h3 class="project-title">Genethink AI</h3>
        <div class="project-content">
            Genethink AI is a quantum-enhanced genomics platform for precision-engineered gene editing. By leveraging AI-optimized CRISPR pathways and advanced genomics, it enables highly accurate and efficient genetic modifications. This platform paves the way for personalized medicine, targeting genetic disorders with unprecedented precision.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="project-card">
        <h3 class="project-title">NexoGPT-1.2</h3>
        <div class="project-content">
            NexoGPT-1.2 is a quantum-accelerated AI advisor that delivers real-time clinical diagnostics and medical intelligence. Designed for healthcare professionals, it provides instant insights, supporting rapid decision-making in critical medical scenarios.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="project-card">
        <h3 class="project-title">NX-News-BIO</h3>
        <div class="project-content">
            NX-News-BIO keeps you informed with curated news and research updates from the cutting-edge fields of quantum biology and AI-driven healthcare innovation. Stay ahead with the latest breakthroughs and trends shaping the future of medicine.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown("""
    <div class="mission-box">
        Our mission is to transform healthcare by synergizing quantum computing and artificial intelligence, making advanced diagnostics and personalized medicine accessible to all.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error rendering page content: {str(e)}")
    logger.error(f"Page content error: {str(e)}")
