"""Session cache and in-memory data storage."""

from typing import Optional, Any, Dict
from datetime import datetime, timedelta
from config.settings import CACHE_TTL
from app.utils.logger import get_logger

logger = get_logger(__name__)


class CacheEntry:
    """Single cache entry with TTL."""
    
    def __init__(self, key: str, value: Any, ttl: int = CACHE_TTL):
        """
        Initialize cache entry.
        
        Args:
            key: Cache key
            value: Cache value
            ttl: Time-to-live in seconds
        """
        self.key = key
        self.value = value
        self.created_at = datetime.now()
        self.ttl = ttl
    
    def is_expired(self) -> bool:
        """
        Check if cache entry is expired.
        
        Returns:
            True if expired
        """
        elapsed = (datetime.now() - self.created_at).total_seconds()
        return elapsed > self.ttl
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "key": self.key,
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "ttl": self.ttl,
            "expired": self.is_expired()
        }


class SessionCache:
    """In-memory session cache."""
    
    def __init__(self):
        """Initialize session cache."""
        self.cache: Dict[str, CacheEntry] = {}
        logger.info("Session cache initialized")
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set cache value.
        
        Args:
            key: Cache key
            value: Cache value
            ttl: Optional time-to-live
        """
        ttl = ttl or CACHE_TTL
        self.cache[key] = CacheEntry(key, value, ttl)
        logger.debug(f"Cache set: {key}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get cache value.
        
        Args:
            key: Cache key
            default: Default value if not found
            
        Returns:
            Cache value or default
        """
        if key not in self.cache:
            return default
        
        entry = self.cache[key]
        if entry.is_expired():
            del self.cache[key]
            logger.debug(f"Cache expired: {key}")
            return default
        
        return entry.value
    
    def delete(self, key: str) -> bool:
        """
        Delete cache entry.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted
        """
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache deleted: {key}")
            return True
        return False
    
    def clear(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of entries cleared
        """
        count = len(self.cache)
        self.cache.clear()
        logger.info(f"Cache cleared: {count} entries")
        return count
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries.
        
        Returns:
            Number of expired entries removed
        """
        expired_keys = [
            key for key, entry in self.cache.items()
            if entry.is_expired()
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        logger.debug(f"Cache cleanup: removed {len(expired_keys)} expired entries")
        return len(expired_keys)
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all valid cache entries.
        
        Returns:
            Dictionary of cache entries
        """
        self.cleanup_expired()
        return {key: entry.value for key, entry in self.cache.items()}
    
    def get_statistics(self) -> dict:
        """
        Get cache statistics.
        
        Returns:
            Statistics dictionary
        """
        total_entries = len(self.cache)
        expired_count = sum(1 for entry in self.cache.values() if entry.is_expired())
        valid_count = total_entries - expired_count
        
        return {
            "total_entries": total_entries,
            "valid_entries": valid_count,
            "expired_entries": expired_count,
            "keys": list(self.cache.keys())
        }
    
    def set_chat_history(self, session_id: str, history: list) -> None:
        """
        Set chat history.
        
        Args:
            session_id: Session ID
            history: Chat history
        """
        self.set(f"chat_history_{session_id}", history)
    
    def get_chat_history(self, session_id: str) -> list:
        """
        Get chat history.
        
        Args:
            session_id: Session ID
            
        Returns:
            Chat history
        """
        return self.get(f"chat_history_{session_id}", [])
    
    def set_document_data(self, session_id: str, data: dict) -> None:
        """
        Set document data.
        
        Args:
            session_id: Session ID
            data: Document data
        """
        self.set(f"document_{session_id}", data)
    
    def get_document_data(self, session_id: str) -> dict:
        """
        Get document data.
        
        Args:
            session_id: Session ID
            
        Returns:
            Document data
        """
        return self.get(f"document_{session_id}", {})


# Global cache instance
_session_cache: Optional[SessionCache] = None


def get_cache() -> SessionCache:
    """
    Get or create session cache.
    
    Returns:
        Session cache instance
    """
    global _session_cache
    if _session_cache is None:
        _session_cache = SessionCache()
    return _session_cache
