"""
MuhammedAI Local Developer - Chat Interface
Chat interface system for web UI.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class MessageType(Enum):
    """Message type."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ERROR = "error"
    INFO = "info"
    WARNING = "warning"
    CUSTOM = "custom"


class MessageStatus(Enum):
    """Message status."""
    SENDING = "sending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    PROCESSING = "processing"


class ChatMode(Enum):
    """Chat mode."""
    NORMAL = "normal"
    CODE = "code"
    DEBUG = "debug"
    EXPLAIN = "explain"
    REFACTOR = "refactor"
    CUSTOM = "custom"


@dataclass
class Message:
    """Chat message."""
    id: str
    type: MessageType
    content: str
    timestamp: datetime
    status: MessageStatus = MessageStatus.SENT
    is_edited: bool = False
    is_deleted: bool = False
    parent_id: Optional[str] = None
    reply_to_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatSession:
    """Chat session."""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = field(default_factory=list)
    is_active: bool = True
    is_archived: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ChatInterfaceConfig:
    """Chat interface configuration."""
    enabled: bool = True
    show_timestamps: bool = True
    show_status: bool = True
    show_avatars: bool = True
    enable_markdown: bool = True
    enable_code_highlighting: bool = True
    enable_emoji: bool = True
    auto_scroll: bool = True
    max_messages: int = 1000
    max_message_length: int = 10000
    enable_edit: bool = True
    enable_delete: bool = True
    enable_reply: bool = True
    enable_forward: bool = True
    enable_search: bool = True


@dataclass
class ChatInterfaceResult:
    """Chat interface result."""
    success: bool
    message: Optional[Message] = None
    messages: List[Message] = field(default_factory=list)
    session: Optional[ChatSession] = None
    errors: List[str] = field(default_factory=list)
    message_text: Optional[str] = None


class ChatInterfaceManager:
    """
    Chat interface manager.
    
    Özellikler:
    - User messages
    - Assistant messages
    - System messages
    - Message editing
    - Message deletion
    - Message replies
    - Message forwarding
    - Chat sessions
    - Message search
    - Message filtering
    - Message status
    - Chat modes
    - Markdown support
    - Code highlighting
    - Emoji support
    - Auto scroll
    """
    
    def __init__(self, config: Optional[ChatInterfaceConfig] = None):
        """
        Initialize chat interface manager.
        
        Args:
            config: Chat interface configuration
        """
        self.config = config or ChatInterfaceConfig()
        self.sessions: Dict[str, ChatSession] = {}
        self.active_session_id: Optional[str] = None
        self.message_id_counter = 0
        self.session_id_counter = 0
        self._next_message_id()
        self._next_session_id()
    
    def _next_message_id(self) -> str:
        """
        Generate next message ID.
        
        Returns:
            str: Message ID
        """
        self.message_id_counter += 1
        return f"msg_{self.message_id_counter}"
    
    def _next_session_id(self) -> str:
        """
        Generate next session ID.
        
        Returns:
            str: Session ID
        """
        self.session_id_counter += 1
        return f"session_{self.session_id_counter}"
    
    def create_session(self, title: str = "New Chat") -> ChatInterfaceResult:
        """
        Create a new chat session.
        
        Args:
            title: Session title
            
        Returns:
            ChatInterfaceResult: Create result
        """
        result = ChatInterfaceResult(success=True)
        
        try:
            now = datetime.now()
            session = ChatSession(
                id=self._next_session_id(),
                title=title,
                created_at=now,
                updated_at=now
            )
            
            self.sessions[session.id] = session
            self.active_session_id = session.id
            result.session = session
            result.message_text = f"Session '{session.id}' created"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def delete_session(self, session_id: str) -> ChatInterfaceResult:
        """
        Delete a chat session.
        
        Args:
            session_id: Session ID
            
        Returns:
            ChatInterfaceResult: Delete result
        """
        result = ChatInterfaceResult(success=False)
        
        try:
            if session_id in self.sessions:
                del self.sessions[session_id]
                if self.active_session_id == session_id:
                    self.active_session_id = None
                result.success = True
                result.message_text = f"Session '{session_id}' deleted"
            else:
                result.errors.append("Session not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Optional[ChatSession]: Session
        """
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[ChatSession]:
        """
        Get all sessions.
        
        Returns:
            List[ChatSession]: All sessions
        """
        return list(self.sessions.values())
    
    def set_active_session(self, session_id: str) -> ChatInterfaceResult:
        """
        Set active session.
        
        Args:
            session_id: Session ID
            
        Returns:
            ChatInterfaceResult: Set result
        """
        result = ChatInterfaceResult(success=False)
        
        try:
            if session_id in self.sessions:
                self.active_session_id = session_id
                result.success = True
                result.message_text = f"Session '{session_id}' set as active"
            else:
                result.errors.append("Session not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def add_message(self, content: str, message_type: MessageType, session_id: Optional[str] = None) -> ChatInterfaceResult:
        """
        Add a message.
        
        Args:
            content: Message content
            message_type: Message type
            session_id: Session ID (uses active if not provided)
            
        Returns:
            ChatInterfaceResult: Add result
        """
        result = ChatInterfaceResult(success=True)
        
        try:
            target_session_id = session_id or self.active_session_id
            
            if not target_session_id:
                result.errors.append("No active session")
                result.success = False
                return result
            
            session = self.sessions.get(target_session_id)
            if not session:
                result.errors.append("Session not found")
                result.success = False
                return result
            
            if len(content) > self.config.max_message_length:
                result.errors.append(f"Message too long (max {self.config.max_message_length})")
                result.success = False
                return result
            
            if len(session.messages) >= self.config.max_messages:
                result.errors.append(f"Maximum messages reached (max {self.config.max_messages})")
                result.success = False
                return result
            
            message = Message(
                id=self._next_message_id(),
                type=message_type,
                content=content,
                timestamp=datetime.now()
            )
            
            session.messages.append(message)
            session.updated_at = datetime.now()
            
            result.message = message
            result.messages = session.messages
            result.message_text = f"Message '{message.id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def edit_message(self, message_id: str, new_content: str, session_id: Optional[str] = None) -> ChatInterfaceResult:
        """
        Edit a message.
        
        Args:
            message_id: Message ID
            new_content: New content
            session_id: Session ID (uses active if not provided)
            
        Returns:
            ChatInterfaceResult: Edit result
        """
        result = ChatInterfaceResult(success=False)
        
        try:
            if not self.config.enable_edit:
                result.errors.append("Edit disabled")
                return result
            
            target_session_id = session_id or self.active_session_id
            session = self.sessions.get(target_session_id)
            
            if not session:
                result.errors.append("Session not found")
                return result
            
            for message in session.messages:
                if message.id == message_id:
                    message.content = new_content
                    message.is_edited = True
                    session.updated_at = datetime.now()
                    result.success = True
                    result.message = message
                    result.message_text = f"Message '{message_id}' edited"
                    break
            else:
                result.errors.append("Message not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def delete_message(self, message_id: str, session_id: Optional[str] = None) -> ChatInterfaceResult:
        """
        Delete a message.
        
        Args:
            message_id: Message ID
            session_id: Session ID (uses active if not provided)
            
        Returns:
            ChatInterfaceResult: Delete result
        """
        result = ChatInterfaceResult(success=False)
        
        try:
            if not self.config.enable_delete:
                result.errors.append("Delete disabled")
                return result
            
            target_session_id = session_id or self.active_session_id
            session = self.sessions.get(target_session_id)
            
            if not session:
                result.errors.append("Session not found")
                return result
            
            for i, message in enumerate(session.messages):
                if message.id == message_id:
                    message.is_deleted = True
                    session.updated_at = datetime.now()
                    result.success = True
                    result.message_text = f"Message '{message_id}' deleted"
                    break
            else:
                result.errors.append("Message not found")
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def reply_to_message(self, message_id: str, content: str, session_id: Optional[str] = None) -> ChatInterfaceResult:
        """
        Reply to a message.
        
        Args:
            message_id: Message ID to reply to
            content: Reply content
            session_id: Session ID (uses active if not provided)
            
        Returns:
            ChatInterfaceResult: Reply result
        """
        result = ChatInterfaceResult(success=True)
        
        try:
            if not self.config.enable_reply:
                result.errors.append("Reply disabled")
                result.success = False
                return result
            
            target_session_id = session_id or self.active_session_id
            session = self.sessions.get(target_session_id)
            
            if not session:
                result.errors.append("Session not found")
                result.success = False
                return result
            
            # Check if original message exists
            original_exists = any(m.id == message_id for m in session.messages)
            if not original_exists:
                result.errors.append("Original message not found")
                result.success = False
                return result
            
            message = Message(
                id=self._next_message_id(),
                type=MessageType.USER,
                content=content,
                timestamp=datetime.now(),
                reply_to_id=message_id
            )
            
            session.messages.append(message)
            session.updated_at = datetime.now()
            
            result.message = message
            result.messages = session.messages
            result.message_text = f"Reply to '{message_id}' added"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_messages(self, session_id: Optional[str] = None) -> List[Message]:
        """
        Get messages from session.
        
        Args:
            session_id: Session ID (uses active if not provided)
            
        Returns:
            List[Message]: Messages
        """
        target_session_id = session_id or self.active_session_id
        session = self.sessions.get(target_session_id)
        
        if session:
            return [m for m in session.messages if not m.is_deleted]
        return []
    
    def search_messages(self, query: str, session_id: Optional[str] = None) -> List[Message]:
        """
        Search messages.
        
        Args:
            query: Search query
            session_id: Session ID (uses active if not provided)
            
        Returns:
            List[Message]: Matching messages
        """
        if not self.config.enable_search:
            return []
        
        target_session_id = session_id or self.active_session_id
        session = self.sessions.get(target_session_id)
        
        if session:
            return [m for m in session.messages if not m.is_deleted and query.lower() in m.content.lower()]
        return []
    
    def get_messages_by_type(self, message_type: MessageType, session_id: Optional[str] = None) -> List[Message]:
        """
        Get messages by type.
        
        Args:
            message_type: Message type
            session_id: Session ID (uses active if not provided)
            
        Returns:
            List[Message]: Messages
        """
        target_session_id = session_id or self.active_session_id
        session = self.sessions.get(target_session_id)
        
        if session:
            return [m for m in session.messages if not m.is_deleted and m.type == message_type]
        return []
    
    def clear_session_messages(self, session_id: Optional[str] = None) -> ChatInterfaceResult:
        """
        Clear all messages in session.
        
        Args:
            session_id: Session ID (uses active if not provided)
            
        Returns:
            ChatInterfaceResult: Clear result
        """
        result = ChatInterfaceResult(success=True)
        
        try:
            target_session_id = session_id or self.active_session_id
            session = self.sessions.get(target_session_id)
            
            if session:
                session.messages.clear()
                session.updated_at = datetime.now()
                result.message_text = f"Session '{target_session_id}' messages cleared"
            else:
                result.errors.append("Session not found")
                result.success = False
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def update_config(self, config: ChatInterfaceConfig) -> ChatInterfaceResult:
        """
        Update chat interface configuration.
        
        Args:
            config: New configuration
            
        Returns:
            ChatInterfaceResult: Update result
        """
        result = ChatInterfaceResult(success=True)
        
        try:
            self.config = config
            result.message_text = "Config updated"
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
            result.success = False
        
        return result
    
    def get_config(self) -> ChatInterfaceConfig:
        """
        Get chat interface configuration.
        
        Returns:
            ChatInterfaceConfig: Configuration
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    config = ChatInterfaceConfig()
    manager = ChatInterfaceManager(config)
    
    # Session oluştur
    result = manager.create_session("Test Chat")
    
    print(f"Session created: {result.message_text}")
    
    # Message ekle
    result = manager.add_message("Hello!", MessageType.USER)
    
    print(f"Message added: {result.message_text}")
    
    # Tüm message'ları al
    messages = manager.get_messages()
    
    print(f"Total messages: {len(messages)}")
