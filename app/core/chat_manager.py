"""Chat management and conversation handling module."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from config.settings import CHAT_HISTORY_LIMIT
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ChatMessage:
    """Represents a single chat message."""
    
    def __init__(self, role: str, content: str, source: Optional[str] = None):
        """
        Initialize chat message.
        
        Args:
            role: Message role ('user' or 'assistant')
            content: Message content
            source: Optional source reference
        """
        self.role = role
        self.content = content
        self.source = source
        self.timestamp = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "source": self.source,
            "timestamp": self.timestamp.isoformat()
        }


class ChatManager:
    """Manages chat conversations and context."""
    
    def __init__(self):
        """Initialize chat manager."""
        self.messages: List[ChatMessage] = []
        self.context: Dict[str, Any] = {}
        logger.info("Chat manager initialized")
    
    def add_user_message(self, content: str) -> ChatMessage:
        """
        Add user message.
        
        Args:
            content: Message content
            
        Returns:
            Chat message object
        """
        message = ChatMessage(role="user", content=content)
        self.messages.append(message)
        logger.debug(f"User message added: {len(content)} chars")
        return message
    
    def add_assistant_message(self, content: str, source: Optional[str] = None) -> ChatMessage:
        """
        Add assistant message.
        
        Args:
            content: Message content
            source: Optional source reference
            
        Returns:
            Chat message object
        """
        message = ChatMessage(role="assistant", content=content, source=source)
        self.messages.append(message)
        logger.debug(f"Assistant message added: {len(content)} chars, source: {source}")
        return message
    
    def get_messages(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get chat messages.
        
        Args:
            limit: Optional message limit
            
        Returns:
            List of messages as dictionaries
        """
        messages_to_return = self.messages
        if limit:
            messages_to_return = self.messages[-limit:]
        
        return [msg.to_dict() for msg in messages_to_return]
    
    def get_context(self) -> str:
        """
        Get formatted context for LLM.
        
        Returns:
            Formatted conversation context
        """
        context_text = ""
        for msg in self.messages[-5:]:  # Last 5 messages for context
            context_text += f"{msg.role.upper()}: {msg.content}\n"
        return context_text
    
    def get_last_user_message(self) -> Optional[str]:
        """
        Get last user message.
        
        Returns:
            Last user message content or None
        """
        for msg in reversed(self.messages):
            if msg.role == "user":
                return msg.content
        return None
    
    def set_context(self, key: str, value: Any) -> None:
        """
        Set context variable.
        
        Args:
            key: Context key
            value: Context value
        """
        self.context[key] = value
        logger.debug(f"Context updated: {key}")
    
    def get_context_value(self, key: str, default: Any = None) -> Any:
        """
        Get context variable.
        
        Args:
            key: Context key
            default: Default value if not found
            
        Returns:
            Context value or default
        """
        return self.context.get(key, default)
    
    def clear_history(self) -> None:
        """Clear chat history."""
        self.messages = []
        logger.info("Chat history cleared")
    
    def clear_context(self) -> None:
        """Clear all context."""
        self.context = {}
        logger.info("Context cleared")
    
    def get_message_count(self) -> int:
        """
        Get total message count.
        
        Returns:
            Number of messages
        """
        return len(self.messages)
    
    def truncate_history(self, max_messages: int = CHAT_HISTORY_LIMIT) -> None:
        """
        Truncate chat history to maximum messages.
        
        Args:
            max_messages: Maximum number of messages to keep
        """
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]
            logger.info(f"Chat history truncated to {max_messages} messages")
    
    def export_conversation(self) -> Dict[str, Any]:
        """
        Export conversation as dictionary.
        
        Returns:
            Conversation data
        """
        return {
            "message_count": len(self.messages),
            "messages": self.get_messages(),
            "context": self.context,
            "export_time": datetime.now().isoformat()
        }
    
    def import_conversation(self, data: Dict[str, Any]) -> bool:
        """
        Import conversation from dictionary.
        
        Args:
            data: Conversation data
            
        Returns:
            True if successful
        """
        try:
            if "messages" in data:
                self.messages = [
                    ChatMessage(
                        role=msg["role"],
                        content=msg["content"],
                        source=msg.get("source")
                    )
                    for msg in data["messages"]
                ]
            
            if "context" in data:
                self.context = data["context"]
            
            logger.info(f"Imported conversation with {len(self.messages)} messages")
            return True
        except Exception as e:
            logger.error(f"Error importing conversation: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get conversation statistics.
        
        Returns:
            Statistics dictionary
        """
        user_messages = [m for m in self.messages if m.role == "user"]
        assistant_messages = [m for m in self.messages if m.role == "assistant"]
        
        total_chars = sum(len(m.content) for m in self.messages)
        user_chars = sum(len(m.content) for m in user_messages)
        assistant_chars = sum(len(m.content) for m in assistant_messages)
        
        return {
            "total_messages": len(self.messages),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "total_characters": total_chars,
            "user_characters": user_chars,
            "assistant_characters": assistant_chars,
            "average_message_length": total_chars // len(self.messages) if self.messages else 0
        }
