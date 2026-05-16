"""Page layouts and views."""

import streamlit as st
from typing import Optional


def upload_page() -> None:
    """Upload page layout."""
    st.title("📤 Upload Document")
    st.markdown("Upload your PDF document to extract information and chat with it.")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("📋 Maximum 2 pages | Max file size: 10MB")


def chat_page() -> None:
    """Chat page layout."""
    st.title("💬 Chat with Document")
    st.markdown("Ask questions about your uploaded document.")


def history_page() -> None:
    """History page layout."""
    st.title("📚 Extraction History")
    st.markdown("View your previous extractions and chats.")


def settings_page() -> None:
    """Settings page layout."""
    st.title("⚙️ Settings")
    st.markdown("Configure application preferences.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("LLM Settings")
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, step=0.1)
        max_tokens = st.slider("Max Tokens", 100, 4000, 2048, step=100)
    
    with col2:
        st.subheader("UI Settings")
        theme = st.selectbox("Theme", ["Light", "Dark"])
        language = st.selectbox("Language", ["English", "Spanish", "French"])
    
    return {"temperature": temperature, "max_tokens": max_tokens, "theme": theme, "language": language}


def home_page() -> None:
    """Home/Dashboard page layout."""
    st.title("🏠 Welcome to DexGA")
    
    st.markdown("""
    ### Document Extraction using Gemma with Localization
    
    Extract information from your documents and chat with them intelligently.
    
    **Features:**
    - 📄 PDF upload and processing
    - 🤖 AI-powered extraction using Gemma
    - 🎯 Source localization
    - 💬 Interactive chat interface
    - 🔒 Privacy-first local processing
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Max Pages", "2")
    with col2:
        st.metric("Max File Size", "10 MB")
    with col3:
        st.metric("Model", "Gemma 7B")


def error_page(error_message: str) -> None:
    """
    Error page layout.
    
    Args:
        error_message: Error message to display
    """
    st.title("❌ Error")
    st.error(error_message)
    st.markdown("Please go back and try again.")
