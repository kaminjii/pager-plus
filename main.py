import streamlit as st
import time
from collections import deque
import random  # For demo purposes, replace with actual log reading

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

st.title('Real-time Log Dashboard')

# Create columns for metrics
col1, col2, col3, col4 = st.columns(4)

# Initialize the placeholder for the log list
log_list = st.empty()

while True:
    # Read new log
    new_log = read_log_line()
    st.session_state.logs.appendleft(new_log)
    
    # Update counts
    st.session_state.counts[new_log['priority']] += 1
    
    # Display metrics
    with col1:
        st.metric("Critical (Red)", st.session_state.counts['red'])
    with col2:
        st.metric("Warning (Yellow)", st.session_state.counts['yellow'])
    with col3:
        st.metric("Info (Green)", st.session_state.counts['green'])
    with col4:
        st.metric("In Progress", st.session_state.counts['in_progress'])
    
    # Display logs with color coding
    with log_list.container():
        for log in st.session_state.logs:
            color_map = {
                'red': '#FF0000',
                'yellow': '#FFA500',
                'green': '#008000',
                'in_progress': '#0000FF'
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