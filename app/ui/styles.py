"""Styling and CSS utilities."""

import streamlit as st


def apply_custom_styles() -> None:
    """Apply custom CSS styles to Streamlit app."""
    st.markdown("""
    <style>
    /* Main container styling */
    .stMainBlockContainer {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #1f77b4;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Code block styling */
    .stCodeBlock {
        background-color: #f0f0f0;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Success/Error/Warning messages */
    .stAlert {
        border-radius: 0.5rem;
        padding: 1rem;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #f9f9f9;
    }
    
    /* Cards */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)


def get_theme_colors(theme: str = "light") -> dict:
    """
    Get color palette based on theme.
    
    Args:
        theme: Theme name ('light' or 'dark')
        
    Returns:
        Dictionary of color values
    """
    themes = {
        "light": {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "error": "#d62728",
            "warning": "#ff9896",
            "info": "#1f77b4",
            "background": "#ffffff",
            "text": "#000000",
        },
        "dark": {
            "primary": "#4a9eff",
            "secondary": "#ffb347",
            "success": "#66ff66",
            "error": "#ff6b6b",
            "warning": "#ffaa00",
            "info": "#4a9eff",
            "background": "#1a1a1a",
            "text": "#ffffff",
        }
    }
    return themes.get(theme, themes["light"])
