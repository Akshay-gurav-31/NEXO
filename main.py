from flask import Flask, render_template, redirect, url_for
import os
import sys
import subprocess
import socket
import time

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Add project directories to Python path
project1_path = os.path.join(project_root, "Eliza_project1", "3d")
project2_path = os.path.join(project_root, "Eliza_project1")
sys.path.extend([project1_path, project2_path])

app = Flask(__name__)

@app.route('/demo')
def demo():
    return render_template('demo.html')

def get_pages():
    """Get all pages from the pages directory in desired menu order."""
    menu_order = [
        ('MRIxAI', '1_MRIxAI.py'),
        ('Genethink AI', '2_Genethink AI.py'),
        ('NexoGPT', '3_NexoGPT.py'),
        ('NewsNX', '4_NewsNX.py'),
        ('About', '5_About.py'),
    ]
    pages = []
    for name, filename in menu_order:
        route = filename.replace(' ', '-').replace('.py', '')  # e.g., '1_MRIxAI.py' -> '1_MRIxAI'
        pages.append({
            'name': name,
            'route': route,
            'file': filename
        })
    return pages

@app.route('/')
def home():
    # Project data
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
    
    # Stats data
    stats = [
        {"number": "2", "label": "Projects"},
        {"number": "86%", "label": "Qubit Fidelity"},
        {"number": "42μs", "label": "Processing Time"}
    ]
    
    # Get all pages for the menu
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

def is_streamlit_running(port):
    """Check if Streamlit server is running on the given port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex(('0.0.0.0', port))
        return result == 0

def start_streamlit():
    """Start Streamlit server for Home.py if not running."""
    port = int(os.getenv('PORT', '8501'))  # Use $PORT for Render
    if not is_streamlit_running(port):
        subprocess.Popen([
            'python', '-m', 'streamlit', 'run', 'Home.py',
            '--server.headless', 'true',
            '--server.port', str(port),
            '--server.address', '0.0.0.0',
            '--server.runOnSave', 'false'
        ], cwd=project_root)
        for _ in range(20):
            if is_streamlit_running(port):
                print(f"[DEBUG] Streamlit for Home.py started on port {port}")
                break
            time.sleep(0.5)
        else:
            print(f"[ERROR] Streamlit for Home.py did not start on port {port}")

# Disable dynamic Streamlit launches for other pages (use multi-page Streamlit or separate service)
@app.route('/embed/<filename>')
def embed(filename):
    # Redirect to Streamlit app (assumes Home.py handles all pages)
    return redirect(f"/")  # Modify to point to Streamlit service if separate

# Start Streamlit for Home.py
start_streamlit()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
