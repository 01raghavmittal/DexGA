"""Reusable Streamlit UI components."""

import streamlit as st
from typing import Optional, Callable, Any
import pandas as pd


def header(title: str, subtitle: Optional[str] = None) -> None:
    """
    Display a header with optional subtitle.
    
    Args:
        title: Main header text
        subtitle: Optional subtitle text
    """
    st.markdown(f"# {title}")
    if subtitle:
        st.markdown(f"*{subtitle}*")


def file_uploader(
    label: str = "Upload a PDF",
    file_type: str = "pdf",
    key: Optional[str] = None
) -> Optional[Any]:
    """
    Custom file uploader component.
    
    Args:
        label: Uploader label
        file_type: Allowed file type
        key: Streamlit component key
        
    Returns:
        Uploaded file or None
    """
    return st.file_uploader(label, type=file_type, key=key)


def chat_message(
    role: str,
    content: str,
    source: Optional[str] = None
) -> None:
    """
    Display a chat message with optional source reference.
    
    Args:
        role: Message role ('user' or 'assistant')
        content: Message content
        source: Optional source reference
    """
    with st.chat_message(role):
        st.markdown(content)
        if source:
            st.caption(f"📍 Source: {source}")


def chat_input_field(
    placeholder: str = "Type your message...",
    key: Optional[str] = None
) -> Optional[str]:
    """
    Custom chat input component.
    
    Args:
        placeholder: Input placeholder text
        key: Streamlit component key
        
    Returns:
        User input text or None
    """
    return st.chat_input(placeholder, key=key)


def document_preview(
    text: str,
    max_chars: int = 1000,
    height: int = 300
) -> None:
    """
    Display document preview in expandable section.
    
    Args:
        text: Document text
        max_chars: Maximum characters to show
        height: Container height in pixels
    """
    with st.expander("📄 Document Preview"):
        display_text = text[:max_chars] + "..." if len(text) > max_chars else text
        st.text_area(
            "Content:",
            value=display_text,
            height=height,
            disabled=True,
            key="doc_preview"
        )


def source_highlight(
    page_num: int,
    text: str,
    confidence: Optional[float] = None
) -> None:
    """
    Display highlighted source information.
    
    Args:
        page_num: Page number
        text: Extracted text
        confidence: Optional confidence score
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"**Page {page_num}**: {text}")
    with col2:
        if confidence:
            st.metric("Confidence", f"{confidence:.1%}")


def loading_spinner(text: str = "Processing...") -> Any:
    """
    Display loading spinner.
    
    Args:
        text: Loading message
        
    Returns:
        Streamlit spinner context
    """
    return st.spinner(text)


def success_message(text: str) -> None:
    """Display success message."""
    st.success(text)


def error_message(text: str) -> None:
    """Display error message."""
    st.error(text)


def warning_message(text: str) -> None:
    """Display warning message."""
    st.warning(text)


def info_message(text: str) -> None:
    """Display info message."""
    st.info(text)


def metric_cards(metrics: dict) -> None:
    """
    Display metrics in cards.
    
    Args:
        metrics: Dictionary of metric_name: metric_value
    """
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
        with col:
            st.metric(label, value)


def data_table(
    data: pd.DataFrame,
    key: Optional[str] = None,
    use_container_width: bool = True
) -> None:
    """
    Display data table.
    
    Args:
        data: DataFrame to display
        key: Component key
        use_container_width: Use full container width
    """
    st.dataframe(data, use_container_width=use_container_width, key=key)


def action_button(
    label: str,
    callback: Callable,
    key: str,
    variant: str = "primary"
) -> bool:
    """
    Display action button.
    
    Args:
        label: Button label
        callback: Callback function
        key: Button key
        variant: Button style variant
        
    Returns:
        Button click status
    """
    return st.button(label, key=key, type=variant)


def sidebar_menu(options: list) -> str:
    """
    Display sidebar navigation menu.
    
    Args:
        options: Menu options
        
    Returns:
        Selected option
    """
    return st.sidebar.radio("Navigation", options)
