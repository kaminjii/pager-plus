import streamlit as st
import time
import pandas as pd
from collections import deque
from datetime import datetime

# Initialize session state
if 'logs' not in st.session_state:
    st.session_state.logs = deque(maxlen=100)  # Keep last 100 logs
    st.session_state.counts = {
        'category': {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0},  # Categories 0-4
        'status': {'in_progress': 0, 'completed': 0},
        'priority': {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
    }

def load_log_data():
    # Sample data structure (you would replace this with your actual data loading)
    data = pd.read_csv('o.csv')  # Replace with your actual file path
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    return data

def get_priority_level(category):
    # Map category numbers to priority levels
    priority_map = {
        '0': 'low',
        '1': 'medium',
        '2': 'medium',
        '3': 'high',
        '4': 'critical'
    }
    return priority_map.get(str(category), 'low')

def process_log_entry(log_entry):
    category = str(log_entry['Category'])
    completed = bool(log_entry['Completed?'])
    status = 'completed' if completed else 'in_progress'
    priority = get_priority_level(category)
    
    return {
        'timestamp': log_entry['Timestamp'],
        'message': log_entry['Message'],
        'category': category,
        'status': status,
        'priority': priority,
        'completed': completed
    }

st.set_page_config(layout="wide")

# Custom CSS for layout
st.markdown("""
    <style>
        [data-testid="stMetricLabel"] {
            font-weight: bold;
        }
        .metric-container [data-testid="metric-container"] {
            border-radius: 10px;
            padding: 10px;
            margin: 5px;
        }
        .critical-metric [data-testid="metric-container"] {
            background-color: rgba(255, 0, 0, 0.1);
            border: 1px solid rgba(255, 0, 0, 0.2);
        }
        .high-metric [data-testid="metric-container"] {
            background-color: rgba(255, 165, 0, 0.1);
            border: 1px solid rgba(255, 165, 0, 0.2);
        }
        .medium-metric [data-testid="metric-container"] {
            background-color: rgba(255, 255, 0, 0.1);
            border: 1px solid rgba(255, 255, 0, 0.2);
        }
        .low-metric [data-testid="metric-container"] {
            background-color: rgba(0, 128, 0, 0.1);
            border: 1px solid rgba(0, 128, 0, 0.2);
        }
        .status-metric [data-testid="metric-container"] {
            background-color: rgba(128, 128, 128, 0.1);
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
        .main-content {
            margin-top: 20px;
        }
        .log-entry {
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            border-left: 5px solid;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title('Enhanced Log Dashboard')

# Create metric containers
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader('Priority Metrics')
    metric_cols = st.columns(4)
    
    # Priority metrics
    with metric_cols[0]:
        st.markdown('<div class="critical-metric metric-container">', unsafe_allow_html=True)
        critical_metric = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_cols[1]:
        st.markdown('<div class="high-metric metric-container">', unsafe_allow_html=True)
        high_metric = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_cols[2]:
        st.markdown('<div class="medium-metric metric-container">', unsafe_allow_html=True)
        medium_metric = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with metric_cols[3]:
        st.markdown('<div class="low-metric metric-container">', unsafe_allow_html=True)
        low_metric = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.subheader('Status Metrics')
    status_cols = st.columns(2)
    
    with status_cols[0]:
        st.markdown('<div class="status-metric metric-container">', unsafe_allow_html=True)
        in_progress_metric = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with status_cols[1]:
        st.markdown('<div class="status-metric metric-container">', unsafe_allow_html=True)
        completed_metric = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)

# Main content area with logs
st.markdown('<div class="main-content">', unsafe_allow_html=True)
log_list = st.empty()

# Load initial data
log_data = load_log_data()

# Process and display logs
for _, row in log_data.iterrows():
    processed_log = process_log_entry(row)
    st.session_state.logs.appendleft(processed_log)
    
    # Update counts
    st.session_state.counts['category'][processed_log['category']] += 1
    st.session_state.counts['status'][processed_log['status']] += 1
    st.session_state.counts['priority'][processed_log['priority']] += 1
    
    # Update metrics
    critical_metric.metric("Critical", st.session_state.counts['priority']['critical'])
    high_metric.metric("High", st.session_state.counts['priority']['high'])
    medium_metric.metric("Medium", st.session_state.counts['priority']['medium'])
    low_metric.metric("Low", st.session_state.counts['priority']['low'])
    
    in_progress_metric.metric("In Progress", st.session_state.counts['status']['in_progress'])
    completed_metric.metric("Completed", st.session_state.counts['status']['completed'])
    
    # Display logs with color coding
    with log_list.container():
        for log in st.session_state.logs:
            priority_colors = {
                'critical': '#FF0000',
                'high': '#FFA500',
                'medium': '#FFD700',
                'low': '#008000'
            }
            
            status_indicator = "✓" if log['completed'] else "⋯"
            
            st.markdown(
                f"""
                <div class="log-entry" style="
                    background-color: {priority_colors[log['priority']]}20;
                    border-left-color: {priority_colors[log['priority']]}
                ">
                    <strong>{log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</strong> |
                    Category: {log['category']} |
                    Priority: {log['priority'].upper()} |
                    Status: {status_indicator} |
                    {log['message']}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    time.sleep(1)  # Small delay between updates