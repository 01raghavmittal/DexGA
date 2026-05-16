"""Input validation and verification utilities."""

import os
from pathlib import Path
from typing import Optional, Tuple
from config.settings import MAX_PDF_PAGES, MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS, MIN_QUERY_LENGTH, MAX_QUERY_LENGTH
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_pdf_file(file_path: str) -> Tuple[bool, str]:
    """
    Validate PDF file.
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        
        # Check file extension
        ext = Path(file_path).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            return False, f"Invalid file format. Allowed: {ALLOWED_EXTENSIONS}"
        
        # Check file size
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            return False, f"File too large. Max: {MAX_FILE_SIZE_MB}MB, Got: {file_size_mb:.2f}MB"
        
        # Check if file is empty
        if os.path.getsize(file_path) == 0:
            return False, "File is empty"
        
        logger.info(f"PDF file validated: {file_path}")
        return True, "File is valid"
    
    except Exception as e:
        logger.error(f"Error validating PDF file: {str(e)}")
        return False, f"Validation error: {str(e)}"


def validate_page_count(page_count: int) -> Tuple[bool, str]:
    """
    Validate PDF page count.
    
    Args:
        page_count: Number of pages
        
    Returns:
        Tuple of (is_valid, message)
    """
    if page_count <= 0:
        return False, "Document has no pages"
    
    if page_count > MAX_PDF_PAGES:
        return False, f"Document exceeds max pages ({MAX_PDF_PAGES}). Got: {page_count}"
    
    return True, "Page count is valid"


def validate_query(query: str) -> Tuple[bool, str]:
    """
    Validate user query.
    
    Args:
        query: User query string
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Check if empty
    if not query or not query.strip():
        return False, "Query cannot be empty"
    
    # Check length
    query_len = len(query.strip())
    if query_len < MIN_QUERY_LENGTH:
        return False, f"Query too short. Min: {MIN_QUERY_LENGTH} characters"
    
    if query_len > MAX_QUERY_LENGTH:
        return False, f"Query too long. Max: {MAX_QUERY_LENGTH} characters"
    
    return True, "Query is valid"


def validate_base64(data: str) -> Tuple[bool, str]:
    """
    Validate Base64 encoded data.
    
    Args:
        data: Base64 string
        
    Returns:
        Tuple of (is_valid, message)
    """
    import base64
    
    try:
        if isinstance(data, str):
            data = data.encode('utf-8')
        base64.b64decode(data, validate=True)
        return True, "Valid Base64"
    except Exception as e:
        logger.error(f"Base64 validation error: {str(e)}")
        return False, f"Invalid Base64: {str(e)}"


def validate_text_content(text: str) -> Tuple[bool, str]:
    """
    Validate extracted text content.
    
    Args:
        text: Text content
        
    Returns:
        Tuple of (is_valid, message)
    """
    if not text or not text.strip():
        return False, "Text content is empty"
    
    if len(text.strip()) < 10:
        return False, "Text content too short"
    
    return True, "Text content is valid"


def validate_session_data(data: dict) -> Tuple[bool, str]:
    """
    Validate session data structure.
    
    Args:
        data: Session data dictionary
        
    Returns:
        Tuple of (is_valid, message)
    """
    required_fields = ["session_id", "created_at"]
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    return True, "Session data is valid"


class Validator:
    """Validation utility class."""
    
    @staticmethod
    def validate_all(
        pdf_path: Optional[str] = None,
        query: Optional[str] = None,
        page_count: Optional[int] = None
    ) -> dict:
        """
        Validate multiple inputs at once.
        
        Args:
            pdf_path: PDF file path
            query: User query
            page_count: Document page count
            
        Returns:
            Dictionary of validation results
        """
        results = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }
        
        if pdf_path:
            valid, msg = validate_pdf_file(pdf_path)
            if not valid:
                results["is_valid"] = False
                results["errors"].append(msg)
        
        if query:
            valid, msg = validate_query(query)
            if not valid:
                results["is_valid"] = False
                results["errors"].append(msg)
        
        if page_count is not None:
            valid, msg = validate_page_count(page_count)
            if not valid:
                results["is_valid"] = False
                results["errors"].append(msg)
        
        return results
