# pages/err.py
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Error Record Report")

st.title("Error Record Report (ERR)")

# Add back navigation
st.markdown('<a href="/" style="color: #FF0000; text-decoration: none;">← Back to Dashboard</a>', unsafe_allow_html=True)

# Get critical errors from session state
if 'logs' in st.session_state:
    critical_errors = [log for log in st.session_state.logs if log['priority'] == 'red']
    
    if critical_errors:
        st.subheader("Critical Error Records")
        
        for i, error in enumerate(critical_errors, start=1):
            with st.container():
                st.markdown(f"### Error {i}")
                col1, col2, col3 = st.columns([2, 3, 3])
                with col1:
                    st.write("**Timestamp:**")
                    st.write(error["timestamp"])
                with col2:
                    st.write("**Error Message:**")
                    st.write(error["message"])
                with col3:
                    st.write("**Notes:**")
                    st.text_area(f"Add notes for Error {i}", key=f"notes_{i}")
    else:
        st.info("No critical errors recorded yet.")
else:
    st.warning("No log data available. Please return to the main dashboard.")
