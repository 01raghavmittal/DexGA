"""Session management utilities."""

import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config.settings import SESSION_TIMEOUT_MINUTES
from app.utils.logger import get_logger

logger = get_logger(__name__)


class Session:
    """Session management class."""
    
    def __init__(self, session_id: Optional[str] = None):
        """
        Initialize session.
        
        Args:
            session_id: Optional session ID
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.metadata: Dict[str, Any] = {}
        self.chat_history = []
        self.document_data = {}
        logger.info(f"Session created: {self.session_id}")
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.now()
    
    def is_expired(self) -> bool:
        """
        Check if session is expired.
        
        Returns:
            True if expired, False otherwise
        """
        timeout = timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        return datetime.now() - self.last_activity > timeout
    
    def set_metadata(self, key: str, value: Any) -> None:
        """
        Set session metadata.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        self.update_activity()
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        Get session metadata.
        
        Args:
            key: Metadata key
            default: Default value if key not found
            
        Returns:
            Metadata value or default
        """
        return self.metadata.get(key, default)
    
    def add_chat_message(self, role: str, content: str, source: Optional[str] = None) -> None:
        """
        Add message to chat history.
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
            source: Optional source reference
        """
        self.chat_history.append({
            "role": role,
            "content": content,
            "source": source,
            "timestamp": datetime.now()
        })
        self.update_activity()
    
    def get_chat_history(self, limit: Optional[int] = None) -> list:
        """
        Get chat history.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            Chat history
        """
        if limit:
            return self.chat_history[-limit:]
        return self.chat_history
    
    def clear_chat_history(self) -> None:
        """Clear chat history."""
        self.chat_history = []
        self.update_activity()
    
    def set_document_data(self, key: str, data: Any) -> None:
        """
        Set document data.
        
        Args:
            key: Data key
            data: Data value
        """
        self.document_data[key] = data
        self.update_activity()
    
    def get_document_data(self, key: str, default: Any = None) -> Any:
        """
        Get document data.
        
        Args:
            key: Data key
            default: Default value if key not found
            
        Returns:
            Document data or default
        """
        return self.document_data.get(key, default)
    
    def clear_document_data(self) -> None:
        """Clear all document data."""
        self.document_data = {}
        self.update_activity()
    
    def to_dict(self) -> dict:
        """
        Convert session to dictionary.
        
        Returns:
            Session data as dictionary
        """
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "last_activity": self.last_activity.isoformat(),
            "metadata": self.metadata,
            "chat_history": self.chat_history,
            "document_data": self.document_data
        }
    
    def cleanup(self) -> None:
        """Cleanup session resources."""
        self.chat_history = []
        self.document_data = {}
        self.metadata = {}
        logger.info(f"Session cleaned up: {self.session_id}")


class SessionManager:
    """Manages multiple sessions."""
    
    _sessions: Dict[str, Session] = {}
    
    @staticmethod
    def create_session(session_id: Optional[str] = None) -> Session:
        """
        Create a new session.
        
        Args:
            session_id: Optional session ID
            
        Returns:
            New session object
        """
        session = Session(session_id)
        SessionManager._sessions[session.session_id] = session
        return session
    
    @staticmethod
    def get_session(session_id: str) -> Optional[Session]:
        """
        Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session object or None
        """
        session = SessionManager._sessions.get(session_id)
        if session and not session.is_expired():
            session.update_activity()
            return session
        elif session:
            SessionManager.delete_session(session_id)
        return None
    
    @staticmethod
    def delete_session(session_id: str) -> bool:
        """
        Delete session.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in SessionManager._sessions:
            SessionManager._sessions[session_id].cleanup()
            del SessionManager._sessions[session_id]
            logger.info(f"Session deleted: {session_id}")
            return True
        return False
    
    @staticmethod
    def cleanup_expired_sessions() -> int:
        """
        Cleanup expired sessions.
        
        Returns:
            Number of sessions cleaned up
        """
        expired_sessions = [
            sid for sid, session in SessionManager._sessions.items()
            if session.is_expired()
        ]
        for sid in expired_sessions:
            SessionManager.delete_session(sid)
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
        return len(expired_sessions)
    
    @staticmethod
    def get_all_sessions() -> Dict[str, Session]:
        """
        Get all active sessions.
        
        Returns:
            Dictionary of all sessions
        """
        return SessionManager._sessions.copy()
