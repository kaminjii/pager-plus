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
        # Convert to DataFrame for better display
        df = pd.DataFrame(critical_errors)
        
        # Add filters
        st.subheader("Filters")
        col1, col2 = st.columns(2)
        with col1:
            selected_time = st.multiselect(
                "Filter by Time",
                options=sorted(df['timestamp'].unique()),
                default=[]
            )
        with col2:
            selected_message = st.multiselect(
                "Filter by Message",
                options=sorted(df['message'].unique()),
                default=[]
            )
        
        # Apply filters
        if selected_time:
            df = df[df['timestamp'].isin(selected_time)]
        if selected_message:
            df = df[df['message'].isin(selected_message)]
        
        # Display statistics
        st.subheader("Error Statistics")
        stats_cols = st.columns(3)
        with stats_cols[0]:
            st.metric("Total Critical Errors", len(critical_errors))
        with stats_cols[1]:
            st.metric("Unique Error Types", df['message'].nunique())
        with stats_cols[2]:
            st.metric("Most Recent Error", df['timestamp'].max() if not df.empty else "N/A")
        
        # Display detailed error table
        st.subheader("Detailed Error Log")
        st.dataframe(
            df,
            hide_index=True,
            column_config={
                "timestamp": "Time",
                "message": "Error Message",
                "priority": None  # Hide priority column since we know they're all red
            }
        )
    else:
        st.info("No critical errors recorded yet.")
else:
    st.warning("No log data available. Please return to the main dashboard.")