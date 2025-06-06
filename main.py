from flask import Flask, render_template, redirect, url_for
import os
import sys

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Add project directories to Python path
project1_path = os.path.join(project_root, "Eliza_project1", "3d")
project2_path = os.path.join(project_root, "Eliza_project1")
sys.path.extend([project1_path, project2_path])

app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/demo')
def demo():
    return render_template('demo.html')

def get_pages():
    """Get all pages from the pages directory in desired menu order."""
    menu_order = [
        ('MRIxAI', '1_MRIxAI'),
        ('Genethink AI', '2_Genethink_AI'),
        ('NexoGPT', '3_NexoGPT'),
        ('NewsNX', '4_NewsNX'),
        ('About', '5_About'),
    ]
    pages = []
    for name, route in menu_order:
        pages.append({
            'name': name,
            'route': route,
            'file': f"{route}.py"
        })
    return pages

@app.route('/')
def home():
    projects = [
        {
            "icon": "⚛",
            "title": "MRIxAI",
            "description": "Quantum-enhanced neural networks for unmatched precision in medical imaging analysis, detecting anomalies.",
            "features": ["Quantum CNN", "Discovery"]
        },
        {
            "icon": "🧬",
            "title": "Genethink AI",
            "description": "Quantum-enhanced genomics platform for precision-engineered gene editing using AI-optimized CRISPR pathways.",
            "features": ["Genomic AI", "Analysis"]
        },
        {
            "icon": "🤖",
            "title": "NexoGPT-1.2",
            "description": "Quantum-accelerated AI advisor delivering real-time clinical diagnostics with breakthrough medical intelligence.",
            "features": ["Medical AI", "Groq Cloud"]
        }
    ]
    stats = [
        {"number": "2", "label": "Projects"},
        {"number": "86%", "label": "Qubit Fidelity"},
        {"number": "42μs", "label": "Processing Time"}
    ]
    pages = get_pages()
    print('[DEBUG] Pages in home:', pages)
    return render_template('index.html', projects=projects, stats=stats, pages=pages, active_page='home')

@app.route('/page/<page_route>')
def page(page_route):
    pages = get_pages()
    print(f"[DEBUG] Requested page route: {page_route}")
    print(f"[DEBUG] Available routes: {[p['route'] for p in pages]}")
    page_info = next((p for p in pages if p['route'] == page_route), None)
    if page_info is None:
        print(f"[DEBUG] Page not found for route {page_route}, redirecting to home")
        return redirect(url_for('home'))
    print(f"[DEBUG] Rendering page: {page_info}")
    return render_template(
        'page.html',
        page=page_info,
        pages=pages,
        active_page=page_route
    )

@app.route('/embed/<filename>')
def embed(filename):
    # Redirect to Streamlit service
    streamlit_url = f"https://your-streamlit-service.onrender.com/{filename.replace('-', '_')}"
    print(f"[DEBUG] Redirecting to Streamlit URL: {streamlit_url}")
    return redirect(streamlit_url)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
