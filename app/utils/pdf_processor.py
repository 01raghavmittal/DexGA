"""PDF processing utilities using PyMuPDF."""

import fitz  # PyMuPDF
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger(__name__)


class PDFProcessor:
    """PDF processing class using PyMuPDF."""
    
    def __init__(self, pdf_path: str):
        """
        Initialize PDF processor.
        
        Args:
            pdf_path: Path to PDF file
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            RuntimeError: If PDF cannot be opened
        """
        self.pdf_path = pdf_path
        try:
            self.document = fitz.open(pdf_path)
            logger.info(f"PDF opened: {pdf_path}")
        except FileNotFoundError:
            logger.error(f"PDF file not found: {pdf_path}")
            raise
        except Exception as e:
            logger.error(f"Failed to open PDF: {str(e)}")
            raise RuntimeError(f"Failed to open PDF: {str(e)}")
    
    def get_page_count(self) -> int:
        """
        Get total page count.
        
        Returns:
            Number of pages
        """
        return len(self.document)
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get PDF metadata.
        
        Returns:
            Dictionary of metadata
        """
        try:
            metadata = self.document.metadata
            return {
                "title": metadata.get("title", "Unknown"),
                "author": metadata.get("author", "Unknown"),
                "subject": metadata.get("subject", "Unknown"),
                "creator": metadata.get("creator", "Unknown"),
                "producer": metadata.get("producer", "Unknown"),
                "pages": self.get_page_count(),
                "format": metadata.get("format", "PDF"),
            }
        except Exception as e:
            logger.error(f"Error extracting metadata: {str(e)}")
            return {"error": str(e)}
    
    def extract_text(self, page_num: int = 0) -> str:
        """
        Extract text from specific page.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            Extracted text
            
        Raises:
            IndexError: If page number is out of range
        """
        try:
            if page_num < 0 or page_num >= len(self.document):
                raise IndexError(f"Page {page_num} out of range")
            
            page = self.document[page_num]
            text = page.get_text()
            logger.debug(f"Text extracted from page {page_num}: {len(text)} chars")
            return text
        except IndexError as e:
            logger.error(f"Invalid page number: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return ""
    
    def extract_text_with_blocks(self, page_num: int = 0) -> List[Dict[str, Any]]:
        """
        Extract text with block information (position, size).
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            List of text blocks with metadata
        """
        try:
            page = self.document[page_num]
            blocks = page.get_text("blocks")
            
            text_blocks = []
            for block in blocks:
                if block[6] == 0:  # Text block
                    text_blocks.append({
                        "text": block[4],
                        "bbox": block[:4],  # (x0, y0, x1, y1)
                        "block_index": len(text_blocks)
                    })
            
            logger.debug(f"Extracted {len(text_blocks)} text blocks from page {page_num}")
            return text_blocks
        except Exception as e:
            logger.error(f"Error extracting text blocks: {str(e)}")
            return []
    
    def extract_all_text(self) -> str:
        """
        Extract text from all pages.
        
        Returns:
            Concatenated text from all pages
        """
        try:
            all_text = ""
            for page_num in range(self.get_page_count()):
                page_text = self.extract_text(page_num)
                all_text += f"\n--- Page {page_num + 1} ---\n{page_text}"
            
            logger.info(f"Extracted text from all {self.get_page_count()} pages")
            return all_text
        except Exception as e:
            logger.error(f"Error extracting all text: {str(e)}")
            return ""
    
    def extract_images(self, page_num: int = 0) -> List[bytes]:
        """
        Extract images from specific page.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            List of image bytes
        """
        try:
            page = self.document[page_num]
            images = []
            
            for img_index, img in enumerate(page.get_images()):
                xref = img[0]
                pix = fitz.Pixmap(self.document, xref)
                if pix.n - pix.alpha < 4:  # GRAY or RGB
                    image_bytes = pix.tobytes("png")
                else:  # CMYK
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                    image_bytes = pix.tobytes("png")
                images.append(image_bytes)
            
            logger.debug(f"Extracted {len(images)} images from page {page_num}")
            return images
        except Exception as e:
            logger.error(f"Error extracting images: {str(e)}")
            return []
    
    def search_text(self, query: str, page_num: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search for text in PDF.
        
        Args:
            query: Search query
            page_num: Optional specific page number
            
        Returns:
            List of search results with positions
        """
        results = []
        try:
            pages_to_search = [page_num] if page_num is not None else range(self.get_page_count())
            
            for pnum in pages_to_search:
                page = self.document[pnum]
                for rect in page.search_for(query):
                    results.append({
                        "page": pnum,
                        "bbox": tuple(rect),
                        "query": query
                    })
            
            logger.debug(f"Found {len(results)} matches for '{query}'")
            return results
        except Exception as e:
            logger.error(f"Error searching text: {str(e)}")
            return []
    
    def get_page_image(self, page_num: int = 0, zoom: float = 2.0) -> bytes:
        """
        Get page as image.
        
        Args:
            page_num: Page number (0-indexed)
            zoom: Zoom level (default 2.0 = 200%)
            
        Returns:
            Image bytes in PNG format
        """
        try:
            page = self.document[page_num]
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            image_bytes = pix.tobytes("png")
            logger.debug(f"Generated image for page {page_num}")
            return image_bytes
        except Exception as e:
            logger.error(f"Error generating page image: {str(e)}")
            return b""
    
    def get_page_size(self, page_num: int = 0) -> Tuple[float, float]:
        """
        Get page dimensions.
        
        Args:
            page_num: Page number (0-indexed)
            
        Returns:
            Tuple of (width, height)
        """
        try:
            page = self.document[page_num]
            rect = page.rect
            return (rect.width, rect.height)
        except Exception as e:
            logger.error(f"Error getting page size: {str(e)}")
            return (0, 0)
    
    def close(self) -> None:
        """Close the PDF document."""
        try:
            self.document.close()
            logger.info(f"PDF closed: {self.pdf_path}")
        except Exception as e:
            logger.error(f"Error closing PDF: {str(e)}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
