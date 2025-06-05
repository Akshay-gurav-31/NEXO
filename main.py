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
            "title": "Genethink AI",  # Fixed: Changed 'Hannah' to "title"
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
        {"number": "99.99%", "label": "Qubit Fidelity"},
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

def get_page_port(filename):
    """Assign a unique port to each page (starting at 8502)."""
    base_port = 8501
    menu_files = [
        '1_MRIxAI.py',
        '2_Genethink AI.py',
        '3_NexoGPT.py',
        '4_NewsNX.py',
        '5_About.py'
    ]
    if filename in menu_files:
        return base_port + menu_files.index(filename) + 1  # Start from 8502
    return base_port + len(menu_files) + 1

def is_streamlit_running(port=8501):
    """Check if Streamlit server is running on the given port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        return result == 0

@app.route('/embed/<filename>')
def embed(filename):
    # Convert URL filename (e.g., '1-MRIxAI') back to actual filename (e.g., '1_MRIxAI.py')
    real_filename = filename.replace('-', ' ') + '.py'
    print(f"[DEBUG] Requested filename from URL: {filename}")
    print(f"[DEBUG] Converted to real filename: {real_filename}")
    
    # Check if the file exists in the pages directory
    abs_streamlit_script = os.path.join(project_root, 'pages', real_filename)
    if not os.path.exists(abs_streamlit_script):
        print(f"[ERROR] Streamlit script does not exist: {abs_streamlit_script}")
        return redirect(url_for('home'))
    
    # Assign a port for this page
    port = get_page_port(real_filename)
    print(f"[DEBUG] Port assigned for {real_filename}: {port}")
    
    # Start Streamlit if it's not running on the assigned port
    if not is_streamlit_running(port):
        streamlit_script = os.path.join('pages', real_filename)
        cmd = [
            'python', '-m', 'streamlit', 'run', streamlit_script,
            '--server.headless', 'true',
            '--server.port', str(port)
        ]
        print(f"[DEBUG] Running command: {' '.join(cmd)} in {project_root}")
        try:
            subprocess.Popen(cmd, cwd=project_root)
            print(f"[DEBUG] Launched Streamlit on port {port}")
            # Wait for Streamlit to start (max 10s)
            for i in range(20):
                if is_streamlit_running(port):
                    print(f"[DEBUG] Streamlit is now running on port {port}")
                    break
                time.sleep(0.5)
            else:
                print(f"[ERROR] Streamlit did not start on port {port} after 10 seconds.")
                return redirect(url_for('home'))
        except Exception as e:
            print(f"[ERROR] Failed to start Streamlit: {e}")
            return redirect(url_for('home'))
    else:
        print(f"[DEBUG] Streamlit already running on port {port}")
    
    # Construct the Streamlit URL
    streamlit_url = f"http://localhost:{port}"
    page_name = real_filename.replace('.py', '')
    print(f"[DEBUG] Streamlit URL: {streamlit_url}, Page name: {page_name}")
    
    return render_template('embed.html', streamlit_url=streamlit_url, page_name=page_name)


def start_streamlit():
    """Start Streamlit server for Home.py if not running."""
    if not is_streamlit_running(8501):
        subprocess.Popen([
            'python', '-m', 'streamlit', 'run', 'Home.py',
            '--server.headless', 'true',
            '--server.port', '8501',
            '--server.runOnSave', 'false'
        ], cwd=project_root)
        for _ in range(20):
            if is_streamlit_running(8501):
                print("[DEBUG] Streamlit for Home.py started on port 8501")
                break
            time.sleep(0.5)
        else:
            print("[ERROR] Streamlit for Home.py did not start on port 8501")

# Standard Flask run block (no custom Streamlit launching needed)
if __name__ == '__main__':
    app.run(debug=True)
