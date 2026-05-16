"""Image processing and analysis utilities."""

from typing import Optional, List, Dict, Any
from app.utils.logger import get_logger
from app.utils.base64_encoder import Base64Encoder
from app.utils.exceptions import PDFException

logger = get_logger(__name__)


class ImageProcessor:
    """Process and analyze images from documents."""
    
    def __init__(self):
        """Initialize image processor."""
        self.images: Dict[int, bytes] = {}  # page_num -> image bytes
        logger.info("Image processor initialized")
    
    def add_image(self, page_num: int, image_bytes: bytes) -> None:
        """
        Store image from document.
        
        Args:
            page_num: Page number where image is from
            image_bytes: Image bytes
        """
        self.images[page_num] = image_bytes
        logger.debug(f"Image added from page {page_num}: {len(image_bytes)} bytes")
    
    def encode_image(self, image_bytes: bytes) -> Optional[str]:
        """
        Encode image to Base64.
        
        Args:
            image_bytes: Image bytes
            
        Returns:
            Base64 encoded string
        """
        try:
            encoded = Base64Encoder.encode_bytes(image_bytes)
            logger.debug(f"Image encoded to Base64: {len(encoded)} chars")
            return encoded
        except Exception as e:
            logger.error(f"Error encoding image: {str(e)}")
            return None
    
    def encode_all_images(self) -> Dict[int, str]:
        """
        Encode all stored images to Base64.
        
        Returns:
            Dictionary of page_num -> base64_string
        """
        encoded_images = {}
        for page_num, image_bytes in self.images.items():
            encoded = self.encode_image(image_bytes)
            if encoded:
                encoded_images[page_num] = encoded
        
        logger.info(f"Encoded {len(encoded_images)} images to Base64")
        return encoded_images
    
    def get_image(self, page_num: int) -> Optional[bytes]:
        """
        Get image bytes from specific page.
        
        Args:
            page_num: Page number
            
        Returns:
            Image bytes or None
        """
        return self.images.get(page_num)
    
    def get_encoded_image(self, page_num: int) -> Optional[str]:
        """
        Get Base64 encoded image from specific page.
        
        Args:
            page_num: Page number
            
        Returns:
            Base64 encoded string or None
        """
        image_bytes = self.get_image(page_num)
        if image_bytes:
            return self.encode_image(image_bytes)
        return None
    
    def get_all_images(self) -> Dict[int, bytes]:
        """
        Get all images.
        
        Returns:
            Dictionary of all images
        """
        return self.images.copy()
    
    def clear_images(self) -> None:
        """Clear all stored images."""
        count = len(self.images)
        self.images.clear()
        logger.info(f"Cleared {count} images")
    
    def get_image_count(self) -> int:
        """
        Get total image count.
        
        Returns:
            Number of images stored
        """
        return len(self.images)
    
    def has_images(self) -> bool:
        """
        Check if any images are stored.
        
        Returns:
            True if images exist
        """
        return len(self.images) > 0
    
    def get_image_statistics(self) -> Dict[str, Any]:
        """
        Get image statistics.
        
        Returns:
            Statistics dictionary
        """
        total_size = sum(len(img) for img in self.images.values())
        pages_with_images = list(self.images.keys())
        
        return {
            "total_images": len(self.images),
            "total_size_bytes": total_size,
            "pages_with_images": pages_with_images,
            "average_size_bytes": total_size // len(self.images) if self.images else 0
        }
