"""Base64 encoding and decoding utilities."""

import base64
from pathlib import Path
from typing import Optional
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Base64Encoder:
    """Base64 encoding/decoding utilities."""
    
    @staticmethod
    def encode_file(file_path: str) -> Optional[str]:
        """
        Encode file to Base64.
        
        Args:
            file_path: Path to file
            
        Returns:
            Base64 encoded string or None
        """
        try:
            with open(file_path, "rb") as f:
                file_bytes = f.read()
            encoded = base64.b64encode(file_bytes).decode("utf-8")
            logger.debug(f"File encoded to Base64: {file_path}")
            return encoded
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error encoding file: {str(e)}")
            return None
    
    @staticmethod
    def encode_string(text: str) -> str:
        """
        Encode string to Base64.
        
        Args:
            text: Text to encode
            
        Returns:
            Base64 encoded string
        """
        try:
            encoded = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            logger.debug(f"String encoded to Base64")
            return encoded
        except Exception as e:
            logger.error(f"Error encoding string: {str(e)}")
            return ""
    
    @staticmethod
    def encode_bytes(data: bytes) -> str:
        """
        Encode bytes to Base64.
        
        Args:
            data: Bytes to encode
            
        Returns:
            Base64 encoded string
        """
        try:
            encoded = base64.b64encode(data).decode("utf-8")
            return encoded
        except Exception as e:
            logger.error(f"Error encoding bytes: {str(e)}")
            return ""
    
    @staticmethod
    def decode_file(encoded_data: str, output_path: str) -> bool:
        """
        Decode Base64 to file.
        
        Args:
            encoded_data: Base64 encoded string
            output_path: Path to save decoded file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            decoded_bytes = base64.b64decode(encoded_data)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(decoded_bytes)
            logger.debug(f"File decoded from Base64: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error decoding file: {str(e)}")
            return False
    
    @staticmethod
    def decode_string(encoded_data: str) -> Optional[str]:
        """
        Decode Base64 to string.
        
        Args:
            encoded_data: Base64 encoded string
            
        Returns:
            Decoded string or None
        """
        try:
            decoded_bytes = base64.b64decode(encoded_data)
            decoded_string = decoded_bytes.decode("utf-8")
            logger.debug(f"String decoded from Base64")
            return decoded_string
        except Exception as e:
            logger.error(f"Error decoding string: {str(e)}")
            return None
    
    @staticmethod
    def decode_bytes(encoded_data: str) -> Optional[bytes]:
        """
        Decode Base64 to bytes.
        
        Args:
            encoded_data: Base64 encoded string
            
        Returns:
            Decoded bytes or None
        """
        try:
            decoded_bytes = base64.b64decode(encoded_data)
            return decoded_bytes
        except Exception as e:
            logger.error(f"Error decoding bytes: {str(e)}")
            return None
    
    @staticmethod
    def get_file_size(encoded_data: str) -> int:
        """
        Get original file size from encoded data.
        
        Args:
            encoded_data: Base64 encoded string
            
        Returns:
            Original file size in bytes
        """
        try:
            decoded = base64.b64decode(encoded_data)
            return len(decoded)
        except Exception as e:
            logger.error(f"Error calculating size: {str(e)}")
            return 0
    
    @staticmethod
    def is_valid_base64(data: str) -> bool:
        """
        Check if data is valid Base64.
        
        Args:
            data: Data to check
            
        Returns:
            True if valid, False otherwise
        """
        try:
            if isinstance(data, str):
                data_bytes = bytes(data, 'utf-8')
            elif isinstance(data, bytes):
                data_bytes = data
            else:
                return False
            return base64.b64encode(base64.b64decode(data_bytes)) == data_bytes
        except Exception:
            return False


# Convenience functions
def encode_file(file_path: str) -> Optional[str]:
    """Convenience function to encode file."""
    return Base64Encoder.encode_file(file_path)


def encode_string(text: str) -> str:
    """Convenience function to encode string."""
    return Base64Encoder.encode_string(text)


def decode_file(encoded_data: str, output_path: str) -> bool:
    """Convenience function to decode file."""
    return Base64Encoder.decode_file(encoded_data, output_path)


def decode_string(encoded_data: str) -> Optional[str]:
    """Convenience function to decode string."""
    return Base64Encoder.decode_string(encoded_data)
