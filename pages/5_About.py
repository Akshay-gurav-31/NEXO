import streamlit as st

# Back to Home button using Streamlit navigation
if st.button("Back to Home", key="back_to_home"):
    st.switch_page("Home.py")  # Assumes your home page is named Home.py

st.title("About Nexora Projects")

st.markdown(
    """
    **Nexora AI** is at the forefront of quantum computing and artificial intelligence, revolutionizing healthcare and genomics with breakthrough technologies. Our projects harness the power of quantum-enhanced neural networks, AI-optimized gene editing, and real-time medical diagnostics to deliver unmatched precision, speed, and intelligence.
    """
)

st.markdown("---")

st.subheader("Our Projects")

st.markdown("""
- **MRIxAI:** Quantum-enhanced neural networks for next-generation medical imaging and anomaly detection.
- **Genethink AI:** Precision-engineered gene editing using AI-optimized CRISPR pathways and advanced genomics.
- **NexoGPT-1.2:** Quantum-accelerated AI advisor delivering real-time clinical diagnostics and medical intelligence.
- **NX-News-BIO:** Curated news and research updates from the world of quantum biology and AI-driven healthcare innovation.
""")

st.markdown("---")

st.info("Our mission is to transform healthcare through the synergy of quantum computing and artificial intelligence, making advanced diagnostics and personalized medicine accessible to all.")
