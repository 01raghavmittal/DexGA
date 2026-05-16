"""Streamlit main application entry point."""

import streamlit as st
from pathlib import Path
from config.settings import APP_NAME, APP_VERSION, PAGE_LAYOUT, INITIAL_SIDEBAR_STATE
from app.ui import components, pages, styles
from app.utils.logger import get_logger
from app.utils.session_manager import SessionManager, get_session
from app.storage.cleanup import start_cleanup, stop_cleanup

logger = get_logger(__name__)

# Configure Streamlit
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📄",
    layout=PAGE_LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE
)

# Apply custom styles
styles.apply_custom_styles()

# Initialize session
if "session_id" not in st.session_state:
    session = SessionManager.create_session()
    st.session_state.session_id = session.session_id
    logger.info(f"New session created: {session.session_id}")
else:
    session = get_session(st.session_state.session_id)
    if session is None:
        # Session expired, create new one
        session = SessionManager.create_session()
        st.session_state.session_id = session.session_id
        logger.warning("Session expired, creating new one")

# Start cleanup on app load
if "cleanup_started" not in st.session_state:
    start_cleanup()
    st.session_state.cleanup_started = True

# Sidebar
with st.sidebar:
    st.title(f"🏠 {APP_NAME}")
    st.caption(f"v{APP_VERSION}")
    st.divider()
    
    # Navigation
    page = st.radio(
        "Navigation",
        options=["Home", "Upload", "Chat", "History", "Settings"],
        key="page_radio"
    )
    
    st.divider()
    
    # Session info
    with st.expander("ℹ️ Session Info"):
        st.write(f"**Session ID:** `{st.session_state.session_id[:8]}...`")
        st.write(f"**Status:** Active")
        if st.button("End Session", key="end_session"):
            SessionManager.delete_session(st.session_state.session_id)
            st.session_state.clear()
            st.success("Session ended")
            st.rerun()

# Main content
if page == "Home":
    pages.home_page()

elif page == "Upload":
    pages.upload_page()
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = components.file_uploader("Upload PDF", "pdf", key="pdf_upload")
        
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
            st.write(f"File size: {uploaded_file.size / 1024:.2f} KB")

elif page == "Chat":
    pages.chat_page()
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for msg in st.session_state.chat_history:
        components.chat_message(msg["role"], msg["content"], msg.get("source"))
    
    # Chat input
    if prompt := components.chat_input_field("Ask your question here..."):
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt
        })
        components.chat_message("user", prompt)
        
        # Simulate assistant response
        with components.loading_spinner("Generating response..."):
            response = "This is a placeholder response. Connect to Gemma LLM for actual responses."
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })
        components.chat_message("assistant", response)

elif page == "History":
    pages.history_page()
    st.info("No extraction history available yet.")

elif page == "Settings":
    settings = pages.settings_page()

# Footer
st.divider()
st.caption(f"DexGA v{APP_VERSION} | Document Extraction using Gemma")
st.caption("Made with ❤️ by DexGA Team")

# Cleanup on session end
def cleanup_on_exit():
    """Cleanup when session ends."""
    stop_cleanup()
    SessionManager.delete_session(st.session_state.session_id)
    logger.info(f"Session cleaned up: {st.session_state.session_id}")

# Register cleanup callback
try:
    import atexit
    atexit.register(cleanup_on_exit)
except:
    pass

if __name__ == "__main__":
    logger.info("Streamlit app started")
