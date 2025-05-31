import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="About - Nexora Projects",
    page_icon="⚛︎",
    layout="wide"
)

# Custom CSS for About page
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    .about-container {
        background: linear-gradient(135deg, 
            rgba(0, 0, 0, 0.95) 0%, 
            rgba(10, 10, 15, 0.9) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 28px;
        padding: 4rem 3rem;
        margin: 2rem auto;
        backdrop-filter: blur(24px);
        box-shadow: 
            0 24px 48px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        max-width: 1200px;
    }

    .about-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #a0a0a0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 3rem;
        text-align: center;
        letter-spacing: -1px;
    }

    .about-section {
        margin-bottom: 4rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .section-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        color: #ffffff;
        margin-bottom: 2rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .section-title::before {
        content: '⚛︎';
        font-size: 1.8rem;
    }

    .about-text {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        line-height: 1.8;
        margin-bottom: 1.5rem;
        text-align: justify;
    }

    .highlight-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .highlight-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem;
        color: #ffffff;
        margin-bottom: 1rem;
    }

    .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2.5rem;
        margin-top: 2rem;
    }

    .team-member {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.05) 0%, 
            rgba(255, 255, 255, 0.02) 100%);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .team-member:hover {
        transform: translateY(-8px);
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.08) 0%, 
            rgba(255, 255, 255, 0.04) 100%);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .member-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.6rem;
        color: #ffffff;
        margin: 1.5rem 0 0.5rem;
    }

    .member-role {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .member-bio {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-top: 1rem;
    }

    .contact-info {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.05) 0%, 
            rgba(255, 255, 255, 0.02) 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .contact-item {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }

    .contact-item:hover {
        transform: translateX(10px);
        color: #ffffff;
    }

    .contact-icon {
        margin-right: 1.5rem;
        font-size: 1.4rem;
    }

    .achievement-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    .achievement-item {
        background: rgba(255, 255, 255, 0.03);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .achievement-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .achievement-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1rem;
    }

    /* Responsive Design - All Devices */
    @media (max-width: 1200px) {
        .about-container {
            max-width: 95%;
            padding: 3rem 2rem;
        }
        
        .about-title {
            font-size: 3rem;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
        
        .team-grid {
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        }
    }

    @media (max-width: 992px) {
        .about-container {
            padding: 2.5rem 1.5rem;
        }
        
        .about-title {
            font-size: 2.8rem;
        }
        
        .about-section {
            padding: 1.5rem;
        }
        
        .achievement-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    @media (max-width: 768px) {
        .about-container {
            padding: 2rem 1rem;
            margin: 1rem auto;
        }
        
        .about-title {
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }
        
        .section-title {
            font-size: 1.6rem;
        }
        
        .about-text {
            font-size: 1.1rem;
        }
        
        .team-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
        
        .achievement-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .highlight-box {
            padding: 1.5rem;
        }
        
        .contact-info {
            padding: 1.5rem;
        }
    }

    @media (max-width: 576px) {
        .about-container {
            padding: 1.5rem 1rem;
            border-radius: 20px;
        }
        
        .about-title {
            font-size: 2rem;
            letter-spacing: -0.5px;
        }
        
        .section-title {
            font-size: 1.4rem;
        }
        
        .about-text {
            font-size: 1rem;
            line-height: 1.6;
        }
        
        .member-name {
            font-size: 1.4rem;
        }
        
        .member-role {
            font-size: 1rem;
        }
        
        .member-bio {
            font-size: 0.9rem;
        }
        
        .achievement-number {
            font-size: 2rem;
        }
        
        .contact-item {
            font-size: 1rem;
        }
    }

    /* Mobile-specific optimizations */
    @media (max-width: 480px) {
        .about-container {
            margin: 0.5rem;
            padding: 1rem;
        }
        
        .about-section {
            padding: 1rem;
            margin-bottom: 2rem;
        }
        
        .highlight-box {
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .team-member {
            padding: 1.5rem;
        }
        
        .contact-info {
            padding: 1rem;
        }
        
        .contact-icon {
            font-size: 1.2rem;
            margin-right: 1rem;
        }
    }

    /* Tablet-specific optimizations */
    @media (min-width: 768px) and (max-width: 1024px) {
        .about-container {
            max-width: 90%;
        }
        
        .team-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .achievement-grid {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    /* Landscape mode optimizations */
    @media (max-height: 600px) and (orientation: landscape) {
        .about-container {
            margin: 1rem auto;
        }
        
        .about-section {
            margin-bottom: 2rem;
        }
        
        .team-grid {
            grid-template-columns: repeat(3, 1fr);
        }
    }

    /* High-resolution displays */
    @media (min-width: 1920px) {
        .about-container {
            max-width: 1600px;
        }
        
        .about-title {
            font-size: 4rem;
        }
        
        .section-title {
            font-size: 2.2rem;
        }
        
        .about-text {
            font-size: 1.3rem;
        }
    }

    /* Print styles */
    @media print {
        .about-container {
            background: none;
            box-shadow: none;
            border: none;
        }
        
        .about-text, .member-name, .section-title {
            color: #000;
        }
        
        .team-member, .contact-info, .highlight-box {
            border: 1px solid #ccc;
        }
    }
</style>
""", unsafe_allow_html=True)

# About Page Content
st.markdown("""
<div class="about-container">
    <h1 class="about-title">About Nexora Projects</h1>
    
    <div class="about-section">
        <h2 class="section-title">Our Vision & Mission</h2>
        <p class="about-text">
            At Nexora Projects, we stand at the forefront of artificial intelligence and biotechnology innovation. 
            Our vision is to revolutionize healthcare and scientific research through cutting-edge AI solutions that 
            make advanced technology accessible, efficient, and impactful.
        </p>
        <div class="highlight-box">
            <p class="about-text">
                Our mission is to bridge the gap between theoretical AI advancements and practical healthcare applications, 
                creating solutions that not only push technological boundaries but also make a real difference in people's lives. 
                We believe in the power of AI to transform healthcare delivery and scientific discovery.
            </p>
        </div>
    </div>

    <div class="about-section">
        <h2 class="section-title">Our Innovation Hub</h2>
        <p class="about-text">
            We specialize in two revolutionary projects that are reshaping their respective fields:
        </p>
        <div class="highlight-box">
            <h3 class="highlight-title">MRIxAI: Medical Imaging Revolution</h3>
            <p class="about-text">
                MRIxAI represents a breakthrough in medical imaging analysis. Our advanced AI algorithms process and analyze 
                medical images with unprecedented accuracy and speed, enabling healthcare professionals to make faster, 
                more accurate diagnoses. The system continuously learns and improves, adapting to new medical imaging 
                techniques and diagnostic requirements.
            </p>
        </div>
        <div class="highlight-box">
            <h3 class="highlight-title">Genethink AI: DNA Analysis Platform</h3>
            <p class="about-text">
                Genethink AI is our state-of-the-art bioinformatics platform that's transforming genetic research. 
                By combining advanced AI with cutting-edge genomic analysis, we're enabling researchers to unlock 
                the secrets of DNA more efficiently than ever before. Our platform accelerates genetic research 
                while maintaining the highest standards of accuracy and reliability.
            </p>
        </div>
    </div>

    <div class="about-section">
        <h2 class="section-title">Our Achievements</h2>
        <div class="achievement-grid">
            <div class="achievement-item">
                <div class="achievement-number">50+</div>
                <div class="achievement-label">Research Papers Published</div>
            </div>
            <div class="achievement-item">
                <div class="achievement-number">100+</div>
                <div class="achievement-label">Healthcare Partners</div>
            </div>
            <div class="achievement-item">
                <div class="achievement-number">1M+</div>
                <div class="achievement-label">Analyses Completed</div>
            </div>
            <div class="achievement-item">
                <div class="achievement-number">99.9%</div>
                <div class="achievement-label">Accuracy Rate</div>
            </div>
        </div>
    </div>

    <div class="about-section">
        <h2 class="section-title">Our Expert Team</h2>
        <div class="team-grid">
            <div class="team-member">
                <span style="font-size: 3.5rem;">👨‍💻</span>
                <h3 class="member-name">Dr. Alex Chen</h3>
                <p class="member-role">Lead AI Researcher</p>
                <p class="member-bio">
                    PhD in Computer Science from MIT, specializing in deep learning and medical image analysis. 
                    Published over 30 papers in top-tier AI journals.
                </p>
            </div>
            <div class="team-member">
                <span style="font-size: 3.5rem;">👩‍🔬</span>
                <h3 class="member-name">Dr. Sarah Miller</h3>
                <p class="member-role">Bioinformatics Expert</p>
                <p class="member-bio">
                    Leading expert in computational biology with 15+ years of experience in genomic data analysis 
                    and AI applications in biotechnology.
                </p>
            </div>
            <div class="team-member">
                <span style="font-size: 3.5rem;">👨‍🔬</span>
                <h3 class="member-name">Dr. James Wilson</h3>
                <p class="member-role">Medical Imaging Specialist</p>
                <p class="member-bio">
                    Board-certified radiologist with extensive experience in implementing AI solutions in clinical settings. 
                    Pioneer in AI-assisted diagnosis.
                </p>
            </div>
        </div>
    </div>

    <div class="about-section">
        <h2 class="section-title">Connect With Us</h2>
        <div class="contact-info">
            <div class="contact-item">
                <span class="contact-icon">📧</span>
                <span>contact@nexoraprojects.com</span>
            </div>
            <div class="contact-item">
                <span class="contact-icon">🌐</span>
                <span>www.nexoraprojects.com</span>
            </div>
            <div class="contact-item">
                <span class="contact-icon">📍</span>
                <span>Innovation Hub, Tech District, Silicon Valley</span>
            </div>
            <div class="contact-item">
                <span class="contact-icon">📱</span>
                <span>+1 (555) 123-4567</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True) 
