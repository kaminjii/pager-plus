# main_dashboard.py
import streamlit as st
import time
from collections import deque
import random

# Initialize session state
if 'logs' not in st.session_state:
    st.session_state.logs = deque(maxlen=100)  # Keep last 100 logs
    st.session_state.counts = {'red': 0, 'yellow': 0, 'green': 0, 'in_progress': 0}

def read_log_line():
    # Replace this with actual log reading logic
    priorities = ['red', 'yellow', 'green', 'in_progress']
    messages = [
        "Server startup complete",
        "Database connection error",
        "New user registered",
        "Processing payment",
        "Memory usage high"
    ]
    return {
        'timestamp': time.strftime('%H:%M:%S'),
        'priority': random.choice(priorities),
        'message': random.choice(messages)
    }

st.set_page_config(layout="wide")

# Custom CSS for layout with colored backgrounds
st.markdown("""
    <style>
        [data-testid="stMetricLabel"] {
            font-weight: bold;
        }
        /* Custom styling for each metric type */
        .red-metric [data-testid="metric-container"] {
            background-color: rgba(255, 0, 0, 0.1);
            border: 1px solid rgba(255, 0, 0, 0.2);
            border-radius: 10px;
            padding: 10px;
        }
        .yellow-metric [data-testid="metric-container"] {
            background-color: rgba(255, 165, 0, 0.1);
            border: 1px solid rgba(255, 165, 0, 0.2);
            border-radius: 10px;
            padding: 10px;
        }
        .green-metric [data-testid="metric-container"] {
            background-color: rgba(0, 128, 0, 0.1);
            border: 1px solid rgba(0, 128, 0, 0.2);
            border-radius: 10px;
            padding: 10px;
        }
        .progress-metric [data-testid="metric-container"] {
            background-color: rgba(128, 128, 128, 0.1);
            border: 1px solid rgba(128, 128, 128, 0.2);
            border-radius: 10px;
            padding: 10px;
        }
        .main-content {
            margin-top: 20px;
        }
        .err-link {
            color: #FF0000;
            text-decoration: none;
            font-size: 0.8em;
            margin-top: 5px;
            display: block;
        }
        .err-link:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title('Real-time Log Dashboard')

# Create metric containers that will be updated
metric_cols = st.columns(4)

# Wrap each metric in a div with the appropriate class
metric_cols[0].markdown('<div class="red-metric">', unsafe_allow_html=True)
red_metric = metric_cols[0].empty()
# Add ERR link below the red metric
metric_cols[0].markdown('<a href="err" class="err-link">View Error Record Report →</a>', unsafe_allow_html=True)
metric_cols[0].markdown('</div>', unsafe_allow_html=True)

metric_cols[1].markdown('<div class="yellow-metric">', unsafe_allow_html=True)
yellow_metric = metric_cols[1].empty()
metric_cols[1].markdown('</div>', unsafe_allow_html=True)

metric_cols[2].markdown('<div class="green-metric">', unsafe_allow_html=True)
green_metric = metric_cols[2].empty()
metric_cols[2].markdown('</div>', unsafe_allow_html=True)

metric_cols[3].markdown('<div class="progress-metric">', unsafe_allow_html=True)
progress_metric = metric_cols[3].empty()
metric_cols[3].markdown('</div>', unsafe_allow_html=True)

# Main content area with logs
st.markdown('<div class="main-content">', unsafe_allow_html=True)
log_list = st.empty()

while True:
    # Read new log
    new_log = read_log_line()
    st.session_state.logs.appendleft(new_log)
    
    # Update counts
    st.session_state.counts[new_log['priority']] += 1
    
    # Update metrics using the placeholders
    red_metric.metric("Critical (Red)", st.session_state.counts['red'])
    yellow_metric.metric("Warning (Yellow)", st.session_state.counts['yellow'])
    green_metric.metric("Info (Green)", st.session_state.counts['green'])
    progress_metric.metric("In Progress", st.session_state.counts['in_progress'])
    
    # Display logs with color coding
    with log_list.container():
        for log in st.session_state.logs:
            color_map = {
                'red': '#FF0000',
                'yellow': '#FFA500',
                'green': '#008000',
                'in_progress': '#808080'
            }
            st.markdown(
                f"""
                <div style="
                    padding: 10px;
                    border-radius: 5px;
                    margin: 5px 0;
                    background-color: {color_map[log['priority']]}20;
                    border-left: 5px solid {color_map[log['priority']]}
                ">
                    <strong>{log['timestamp']}</strong>: {log['message']}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    time.sleep(1)  # Wait 1 second before next update