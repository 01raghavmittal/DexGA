"""Document handling and processing module."""

from typing import Optional, Dict, Any, Tuple
from pathlib import Path
from app.utils.logger import get_logger
from app.utils.pdf_processor import PDFProcessor
from app.utils.base64_encoder import Base64Encoder
from app.utils.validators import validate_pdf_file, validate_page_count
from app.utils.exceptions import PDFException, ValidationException

logger = get_logger(__name__)


class DocumentHandler:
    """Handles document loading, processing, and management."""
    
    def __init__(self):
        """Initialize document handler."""
        self.current_document: Optional[PDFProcessor] = None
        self.document_data: Dict[str, Any] = {}
        self.base64_encoded_doc: Optional[str] = None
    
    def load_document(self, file_path: str) -> bool:
        """
        Load and validate PDF document.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            # Validate file
            is_valid, msg = validate_pdf_file(file_path)
            if not is_valid:
                logger.error(f"PDF validation failed: {msg}")
                raise ValidationException(msg)
            
            # Open document
            self.current_document = PDFProcessor(file_path)
            
            # Validate page count
            page_count = self.current_document.get_page_count()
            is_valid, msg = validate_page_count(page_count)
            if not is_valid:
                self.current_document.close()
                logger.error(f"Page count validation failed: {msg}")
                raise ValidationException(msg)
            
            # Extract metadata
            self.document_data = {
                "file_path": file_path,
                "file_name": Path(file_path).name,
                "page_count": page_count,
                "metadata": self.current_document.get_metadata()
            }
            
            logger.info(f"Document loaded successfully: {file_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error loading document: {str(e)}")
            raise PDFException(f"Failed to load document: {str(e)}")
    
    def extract_text(self, page_num: Optional[int] = None) -> str:
        """
        Extract text from document.
        
        Args:
            page_num: Optional page number (0-indexed)
            
        Returns:
            Extracted text
        """
        if not self.current_document:
            raise PDFException("No document loaded")
        
        try:
            if page_num is None:
                # Extract from all pages
                text = self.current_document.extract_all_text()
            else:
                # Extract from specific page
                text = self.current_document.extract_text(page_num)
            
            logger.debug(f"Text extracted: {len(text)} characters")
            return text
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise PDFException(f"Failed to extract text: {str(e)}")
    
    def extract_text_with_blocks(self, page_num: int = 0) -> list:
        """
        Extract text with position information.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            List of text blocks with metadata
        """
        if not self.current_document:
            raise PDFException("No document loaded")
        
        try:
            blocks = self.current_document.extract_text_with_blocks(page_num)
            logger.debug(f"Extracted {len(blocks)} text blocks")
            return blocks
        except Exception as e:
            logger.error(f"Error extracting text blocks: {str(e)}")
            return []
    
    def get_document_info(self) -> Dict[str, Any]:
        """
        Get document information.
        
        Returns:
            Dictionary of document info
        """
        if not self.current_document:
            return {}
        
        return {
            "file_name": self.document_data.get("file_name"),
            "page_count": self.document_data.get("page_count"),
            "metadata": self.document_data.get("metadata", {})
        }
    
    def encode_to_base64(self) -> Optional[str]:
        """
        Encode loaded document to Base64.
        
        Returns:
            Base64 encoded string or None
        """
        if not self.current_document:
            raise PDFException("No document loaded")
        
        try:
            encoded = Base64Encoder.encode_file(self.document_data["file_path"])
            self.base64_encoded_doc = encoded
            logger.info("Document encoded to Base64")
            return encoded
        except Exception as e:
            logger.error(f"Error encoding document: {str(e)}")
            return None
    
    def get_page_image(self, page_num: int = 0) -> bytes:
        """
        Get page as image.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            Image bytes
        """
        if not self.current_document:
            raise PDFException("No document loaded")
        
        try:
            image = self.current_document.get_page_image(page_num)
            logger.debug(f"Page image generated: {len(image)} bytes")
            return image
        except Exception as e:
            logger.error(f"Error generating page image: {str(e)}")
            return b""
    
    def extract_images_all_pages(self) -> list:
        """
        Extract all images from all pages.
        
        Returns:
            List of image bytes from all pages
        """
        if not self.current_document:
            raise PDFException("No document loaded")
        
        try:
            all_images = []
            for page_num in range(self.document_data.get("page_count", 0)):
                images = self.current_document.extract_images(page_num)
                all_images.extend([(page_num, img) for img in images])
            
            logger.info(f"Extracted {len(all_images)} images from all pages")
            return all_images
        except Exception as e:
            logger.error(f"Error extracting images: {str(e)}")
            return []
    
    def search_text(self, query: str, page_num: Optional[int] = None) -> list:
        """
        Search for text in document.
        
        Args:
            query: Search query
            page_num: Optional specific page number
            
        Returns:
            List of search results
        """
        if not self.current_document:
            raise PDFException("No document loaded")
        
        try:
            results = self.current_document.search_text(query, page_num)
            logger.debug(f"Found {len(results)} matches for: {query}")
            return results
        except Exception as e:
            logger.error(f"Error searching text: {str(e)}")
            return []
    
    def close_document(self) -> None:
        """Close and cleanup document."""
        try:
            if self.current_document:
                self.current_document.close()
                self.current_document = None
            
            self.document_data = {}
            self.base64_encoded_doc = None
            logger.info("Document closed and cleaned up")
        except Exception as e:
            logger.error(f"Error closing document: {str(e)}")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close_document()
