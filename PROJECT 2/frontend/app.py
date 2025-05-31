import streamlit as st

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Autonomous Hypothesis Generator",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Now import other modules
import sys
import os
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import time
import json
import threading
import random
from collections import defaultdict
import re

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Define paths
HYPOTHESES_FILE = os.path.join(parent_dir, 'app', 'hypotheses.txt')

# Now import app modules after path is set
from app.hypo import HypothesisGenerator
from app.config import GEMINI_API_KEYS, API_CONFIG, SECURITY_CONFIG

# Initialize system state in session state
if 'system_running' not in st.session_state:
    st.session_state.system_running = False
if 'hypotheses' not in st.session_state:
    st.session_state.hypotheses = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = None
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False
if 'generator' not in st.session_state:
    st.session_state.generator = None

# Function to load unique hypotheses from file (latest first, no duplicates)
def load_hypotheses():
    try:
        seen = set()
        hypotheses = []
        with open(HYPOTHESES_FILE, 'r') as f:
            for line in reversed(list(f)):
                try:
                    hypothesis = json.loads(line)
                    # Use id if present, else statement+timestamp as unique key
                    unique_key = str(hypothesis.get('id')) if 'id' in hypothesis else f"{hypothesis.get('statement','')}|{hypothesis.get('timestamp','')}"
                    if unique_key not in seen:
                        hypotheses.append(hypothesis)
                        seen.add(unique_key)
                except json.JSONDecodeError:
                    continue
        return hypotheses
    except Exception as e:
        st.error(f"Error loading hypotheses: {str(e)}")
        return []

# Function to display hypothesis card
def display_hypothesis_card(hypothesis):
    implications = hypothesis.get('implications', [])
    # If implications is a string, split into list by newlines and asterisks
    if isinstance(implications, str):
        # Split on newlines and asterisks, remove empty and strip whitespace
        implications = [i.strip(' *\n\r\t') for i in re.split(r'\n|\*', implications) if i.strip(' *\n\r\t')]
    st.markdown(f"""
    <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; margin: 10px 0; border: 1px solid #64ffda;">
        <h3 style="color: #64ffda; margin-bottom: 15px;">{hypothesis.get('statement', '')}</h3>
        <div style="background-color: #2D2D2D; padding: 15px; border-radius: 5px; margin-bottom: 15px;">
            <p style="margin: 0;"><strong style="color: #64ffda;">Background:</strong> {hypothesis.get('background', '')}</p>
        </div>
        <div style="margin: 15px 0;">
            <strong style="color: #64ffda;">Implications:</strong>
            <div style="background-color: #2D2D2D; padding: 15px; border-radius: 5px; margin-top: 10px;">
                <ul style='margin: 0; padding-left: 20px;'>
                    {''.join(f'<li style="margin: 5px 0; line-height: 1.5;">{imp}</li>' for imp in implications)}
                </ul>
            </div>
        </div>
        <p style="color: #888; font-size: 0.8em; margin: 0;">Generated at: {hypothesis.get('timestamp', '')}</p>
    </div>
    """, unsafe_allow_html=True)

# Function to get the next hypothesis index
def get_next_hypothesis_index():
    try:
        with open(HYPOTHESES_FILE, 'r') as f:
            last = None
            for line in f:
                try:
                    hypo = json.loads(line)
                    last = hypo
                except Exception:
                    continue
            if last and 'id' in last:
                return int(last['id']) + 1
            else:
                return 1
    except Exception:
        return 1

# Theme toggle in sidebar with responsive design
with st.sidebar:
    st.markdown("### System Control")
    
    # System status display
    status_color = "green" if st.session_state.system_running else "red"
    status_text = "Running" if st.session_state.system_running else "Stopped"
    st.markdown(f"""
    <div style="background-color: #1E1E1E; padding: 10px; border-radius: 5px; margin: 10px 0; border: 1px solid {status_color};">
        <div style="color: {status_color}; font-weight: bold; text-align: center;">System Status: {status_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("▶️ Start", disabled=st.session_state.system_running, use_container_width=True):
            # Initialize generator when starting
            st.session_state.generator = HypothesisGenerator(GEMINI_API_KEYS)
            st.session_state.system_running = True
            st.session_state.last_update = datetime.now()
            st.rerun()
    with col2:
        if st.button("⏹️ Stop", disabled=not st.session_state.system_running, use_container_width=True):
            # Clear generator when stopping
            st.session_state.generator = None
            st.session_state.system_running = False
            st.rerun()
    
    st.markdown("---")
    
    # Generate button
    if st.session_state.system_running and st.session_state.generator:
        if st.button("🔬 Generate Hypothesis", disabled=st.session_state.is_generating, use_container_width=True):
            st.session_state.is_generating = True
            try:
                new_hypothesis = st.session_state.generator.generate_hypothesis()
                if new_hypothesis:
                    # Assign next index/id
                    new_hypothesis['id'] = get_next_hypothesis_index()
                    new_hypothesis['timestamp'] = datetime.now().isoformat()
                    try:
                        with open(HYPOTHESES_FILE, 'a') as f:
                            f.write(json.dumps(new_hypothesis) + '\n')
                    except Exception as e:
                        st.error(f"Error saving hypothesis: {str(e)}")
                    st.session_state.hypotheses = load_hypotheses()
                    st.session_state.last_update = datetime.now()
                    st.success("New hypothesis generated!")
                    st.rerun()
            except Exception as e:
                # On error, show a random saved hypothesis if available
                st.error(f"API error: {str(e)}. Showing a random saved hypothesis.")
                saved_hypos = load_hypotheses()
                if saved_hypos:
                    random_hypo = random.choice(saved_hypos)
                    st.session_state.hypotheses = [random_hypo]
                    st.rerun()
                else:
                    st.error("No saved hypotheses available.")
            finally:
                st.session_state.is_generating = False
    else:
        st.info("Start the system to generate hypotheses")

# Main content area
st.title("Autonomous Hypothesis Generator")

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🔬 Latest Hypothesis")
    hypotheses_list = load_hypotheses()
    st.session_state.hypotheses = hypotheses_list
    if st.session_state.system_running:
        if hypotheses_list:
            display_hypothesis_card(hypotheses_list[0])
        else:
            st.info("No hypothesis generated yet. Click 'Generate Hypothesis' in the sidebar to create one.")
    else:
        st.info("System is currently stopped. Click 'Start' in the sidebar to begin.")

with col2:
    st.markdown("### 📊 Statistics")
    # Always use file-based count
    hypotheses_list = load_hypotheses()
    if hypotheses_list:
        total_hypotheses = len(hypotheses_list)
        st.metric("Total Hypotheses", total_hypotheses)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        recent_hypotheses = sum(1 for h in hypotheses_list if datetime.fromisoformat(h.get('timestamp', '')) > one_hour_ago)
        st.metric("Last Hour", recent_hypotheses)
        if len(hypotheses_list) > 1:
            timestamps = [datetime.fromisoformat(h.get('timestamp', '')) for h in hypotheses_list]
            df = pd.DataFrame({'timestamp': timestamps})
            df['count'] = 1
            df = df.set_index('timestamp').resample('H').count()
            fig = px.line(df, title="Hypotheses Generated Over Time", labels={'timestamp': 'Time', 'count': 'Number of Hypotheses'})
            fig.update_layout(plot_bgcolor='#1E1E1E', paper_bgcolor='#1E1E1E', font_color='white', title_font_color='#64ffda')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No statistics available yet. Generate some hypotheses to see statistics.") 