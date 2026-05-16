"""Automatic cleanup and maintenance routines."""

import os
import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Callable
from config.settings import AUTO_CLEANUP_ENABLED, CLEANUP_INTERVAL_HOURS, TEMP_DIR
from app.utils.logger import get_logger
from app.storage.local_storage import LocalStorage
from app.storage.session_cache import get_cache

logger = get_logger(__name__)


class CleanupManager:
    """Manages automatic cleanup of temporary files and cache."""
    
    def __init__(self, enabled: bool = AUTO_CLEANUP_ENABLED):
        """
        Initialize cleanup manager.
        
        Args:
            enabled: Whether cleanup is enabled
        """
        self.enabled = enabled
        self.cleanup_thread: Optional[threading.Thread] = None
        self.running = False
        logger.info(f"Cleanup manager initialized (enabled={enabled})")
    
    def cleanup_temp_files(self, age_hours: int = 24) -> int:
        """
        Clean up old temporary files.
        
        Args:
            age_hours: Age threshold in hours
            
        Returns:
            Number of files deleted
        """
        try:
            old_files = LocalStorage.get_old_files(str(TEMP_DIR), age_hours)
            deleted_count = 0
            
            for file_path in old_files:
                if LocalStorage.delete_file(file_path):
                    deleted_count += 1
            
            logger.info(f"Temp file cleanup: deleted {deleted_count} files older than {age_hours}h")
            return deleted_count
        except Exception as e:
            logger.error(f"Error cleaning temp files: {str(e)}")
            return 0
    
    def cleanup_cache_expired(self) -> int:
        """
        Clean up expired cache entries.
        
        Returns:
            Number of entries removed
        """
        try:
            cache = get_cache()
            count = cache.cleanup_expired()
            logger.info(f"Cache cleanup: removed {count} expired entries")
            return count
        except Exception as e:
            logger.error(f"Error cleaning cache: {str(e)}")
            return 0
    
    def full_cleanup(self) -> dict:
        """
        Perform full cleanup (temp files + cache).
        
        Returns:
            Cleanup statistics
        """
        stats = {
            "timestamp": datetime.now().isoformat(),
            "temp_files_deleted": 0,
            "cache_entries_removed": 0
        }
        
        try:
            stats["temp_files_deleted"] = self.cleanup_temp_files()
            stats["cache_entries_removed"] = self.cleanup_cache_expired()
            logger.info(f"Full cleanup completed: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error during full cleanup: {str(e)}")
            return stats
    
    def start_periodic_cleanup(
        self,
        interval_hours: int = CLEANUP_INTERVAL_HOURS,
        age_hours: int = 24
    ) -> None:
        """
        Start periodic cleanup thread.
        
        Args:
            interval_hours: Cleanup interval in hours
            age_hours: File age threshold in hours
        """
        if not self.enabled:
            logger.warning("Periodic cleanup is disabled")
            return
        
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            logger.warning("Cleanup thread already running")
            return
        
        def cleanup_worker():
            """Worker function for cleanup thread."""
            self.running = True
            logger.info(f"Periodic cleanup started (interval: {interval_hours}h, age: {age_hours}h)")
            
            while self.running:
                try:
                    time.sleep(interval_hours * 3600)
                    if self.running:
                        self.full_cleanup()
                except Exception as e:
                    logger.error(f"Error in cleanup worker: {str(e)}")
        
        self.cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        self.cleanup_thread.start()
    
    def stop_periodic_cleanup(self) -> None:
        """Stop periodic cleanup thread."""
        self.running = False
        if self.cleanup_thread:
            self.cleanup_thread.join(timeout=5)
        logger.info("Periodic cleanup stopped")
    
    def cleanup_session(self, session_id: str) -> bool:
        """
        Clean up specific session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if successful
        """
        try:
            cache = get_cache()
            
            # Remove session data from cache
            cache.delete(f"chat_history_{session_id}")
            cache.delete(f"document_{session_id}")
            
            logger.info(f"Session cleaned up: {session_id}")
            return True
        except Exception as e:
            logger.error(f"Error cleaning session: {str(e)}")
            return False
    
    def get_cleanup_status(self) -> dict:
        """
        Get cleanup status.
        
        Returns:
            Status dictionary
        """
        try:
            cache = get_cache()
            cache_stats = cache.get_statistics()
            
            temp_dir_size = LocalStorage.get_directory_size(str(TEMP_DIR))
            temp_file_count = len(LocalStorage.list_files(str(TEMP_DIR)))
            
            return {
                "enabled": self.enabled,
                "running": self.running and (self.cleanup_thread and self.cleanup_thread.is_alive()),
                "temp_files": temp_file_count,
                "temp_directory_size": temp_dir_size,
                "cache_statistics": cache_stats
            }
        except Exception as e:
            logger.error(f"Error getting cleanup status: {str(e)}")
            return {}


# Global cleanup manager instance
_cleanup_manager: Optional[CleanupManager] = None


def get_cleanup_manager() -> CleanupManager:
    """
    Get or create cleanup manager.
    
    Returns:
        Cleanup manager instance
    """
    global _cleanup_manager
    if _cleanup_manager is None:
        _cleanup_manager = CleanupManager()
    return _cleanup_manager


def start_cleanup() -> None:
    """Start automatic cleanup."""
    manager = get_cleanup_manager()
    manager.start_periodic_cleanup()


def stop_cleanup() -> None:
    """Stop automatic cleanup."""
    manager = get_cleanup_manager()
    manager.stop_periodic_cleanup()
