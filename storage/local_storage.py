"""Local storage operations for temporary files and session data."""

import os
import shutil
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from config.settings import TEMP_DIR
from app.utils.logger import get_logger
from app.utils.exceptions import StorageException

logger = get_logger(__name__)


class LocalStorage:
    """Local file storage management."""
    
    @staticmethod
    def ensure_directory_exists(dir_path: str) -> bool:
        """
        Ensure directory exists.
        
        Args:
            dir_path: Directory path
            
        Returns:
            True if directory exists or was created
        """
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            logger.debug(f"Directory ready: {dir_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating directory: {str(e)}")
            return False
    
    @staticmethod
    def save_file(source_path: str, dest_dir: str = str(TEMP_DIR)) -> Optional[str]:
        """
        Save file to temporary directory.
        
        Args:
            source_path: Source file path
            dest_dir: Destination directory
            
        Returns:
            Destination file path or None
        """
        try:
            if not os.path.exists(source_path):
                raise FileNotFoundError(f"Source file not found: {source_path}")
            
            LocalStorage.ensure_directory_exists(dest_dir)
            filename = Path(source_path).name
            dest_path = os.path.join(dest_dir, filename)
            
            shutil.copy2(source_path, dest_path)
            logger.info(f"File saved: {dest_path}")
            return dest_path
        
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise StorageException(f"Failed to save file: {str(e)}")
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete file.
        
        Args:
            file_path: File path
            
        Returns:
            True if deleted successfully
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    @staticmethod
    def list_files(directory: str = str(TEMP_DIR)) -> List[str]:
        """
        List files in directory.
        
        Args:
            directory: Directory path
            
        Returns:
            List of file paths
        """
        try:
            if not os.path.exists(directory):
                return []
            
            files = [
                os.path.join(directory, f)
                for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))
            ]
            logger.debug(f"Listed {len(files)} files in {directory}")
            return files
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            return []
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: File path
            
        Returns:
            File size in bytes
        """
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
            return 0
        except Exception as e:
            logger.error(f"Error getting file size: {str(e)}")
            return 0
    
    @staticmethod
    def get_directory_size(directory: str = str(TEMP_DIR)) -> int:
        """
        Get total directory size.
        
        Args:
            directory: Directory path
            
        Returns:
            Total size in bytes
        """
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            return total_size
        except Exception as e:
            logger.error(f"Error calculating directory size: {str(e)}")
            return 0
    
    @staticmethod
    def clear_directory(directory: str = str(TEMP_DIR)) -> int:
        """
        Clear all files in directory.
        
        Args:
            directory: Directory path
            
        Returns:
            Number of files deleted
        """
        try:
            files = LocalStorage.list_files(directory)
            deleted_count = 0
            
            for file_path in files:
                if LocalStorage.delete_file(file_path):
                    deleted_count += 1
            
            logger.info(f"Cleared {deleted_count} files from {directory}")
            return deleted_count
        except Exception as e:
            logger.error(f"Error clearing directory: {str(e)}")
            return 0
    
    @staticmethod
    def get_old_files(
        directory: str = str(TEMP_DIR),
        age_hours: int = 24
    ) -> List[str]:
        """
        Get files older than specified age.
        
        Args:
            directory: Directory path
            age_hours: Age threshold in hours
            
        Returns:
            List of old file paths
        """
        try:
            import time
            old_files = []
            current_time = time.time()
            threshold = age_hours * 3600
            
            for file_path in LocalStorage.list_files(directory):
                file_time = os.path.getmtime(file_path)
                if current_time - file_time > threshold:
                    old_files.append(file_path)
            
            logger.debug(f"Found {len(old_files)} files older than {age_hours} hours")
            return old_files
        except Exception as e:
            logger.error(f"Error finding old files: {str(e)}")
            return []
