# pages/err.py
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Error Record Report")

st.title("Error Record Report (ERR)")

# Add back navigation
st.markdown('<a href="/" style="color: #FF0000; text-decoration: none;">← Back to Dashboard</a>', unsafe_allow_html=True)

# Ensure the notes dictionary and editing states are initialized in session state
if 'notes' not in st.session_state:
    st.session_state['notes'] = {}
if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = {}

# Get critical errors from session state
if 'logs' in st.session_state:
    critical_errors = [log for log in st.session_state.logs if log['priority'] == 'red']
    
    if critical_errors:
        st.subheader("Critical Error Records")
        
        for i, error in enumerate(critical_errors, start=1):
            error_id = f"error_{i}"  # Unique ID for each error

            # Initialize notes and edit state for this error
            if error_id not in st.session_state['notes']:
                st.session_state['notes'][error_id] = ""  # Default empty notes
            if error_id not in st.session_state['edit_mode']:
                st.session_state['edit_mode'][error_id] = False  # Default to not editing
            
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
                    if st.session_state['edit_mode'][error_id]:
                        # Editable text area
                        new_notes = st.text_area(
                            "Edit Notes", 
                            value=st.session_state['notes'][error_id], 
                            key=f"notes_edit_{i}"
                        )
                        # Save button
                        if st.button("Save", key=f"save_button_{i}"):
                            st.session_state['notes'][error_id] = new_notes
                            st.session_state['edit_mode'][error_id] = False
                    else:
                        # Display saved notes
                        st.write("**Notes:**")
                        st.write(st.session_state['notes'][error_id] or "No notes yet.")
                        # Edit button
                        if st.button("Edit", key=f"edit_button_{i}"):
                            st.session_state['edit_mode'][error_id] = True
    else:
        st.info("No critical errors recorded yet.")
else:
    st.warning("No log data available. Please return to the main dashboard.")
