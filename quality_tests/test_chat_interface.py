"""
Quality Test: Chat Interface
Chat interface system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.chat_interface import (
    MessageType,
    MessageStatus,
    ChatMode,
    Message,
    ChatSession,
    ChatInterfaceConfig,
    ChatInterfaceResult,
    ChatInterfaceManager
)
from datetime import datetime


def test_message_type_enum():
    """
    Test: MessageType enum.
    """
    print("=" * 70)
    print("TEST: MessageType Enum")
    print("=" * 70)
    
    assert MessageType.USER.value == "user"
    assert MessageType.ASSISTANT.value == "assistant"
    assert MessageType.SYSTEM.value == "system"
    assert MessageType.ERROR.value == "error"
    assert MessageType.INFO.value == "info"
    assert MessageType.WARNING.value == "warning"
    assert MessageType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(MessageType)}")
    
    print("\n" + "=" * 70)
    print("PASS: MessageType enum")
    print("=" * 70)


def test_message_status_enum():
    """
    Test: MessageStatus enum.
    """
    print("=" * 70)
    print("TEST: MessageStatus Enum")
    print("=" * 70)
    
    assert MessageStatus.SENDING.value == "sending"
    assert MessageStatus.SENT.value == "sent"
    assert MessageStatus.DELIVERED.value == "delivered"
    assert MessageStatus.READ.value == "read"
    assert MessageStatus.FAILED.value == "failed"
    assert MessageStatus.PROCESSING.value == "processing"
    
    print(f"  All enum values verified")
    print(f"  Total statuses: {len(MessageStatus)}")
    
    print("\n" + "=" * 70)
    print("PASS: MessageStatus enum")
    print("=" * 70)


def test_chat_mode_enum():
    """
    Test: ChatMode enum.
    """
    print("=" * 70)
    print("TEST: ChatMode Enum")
    print("=" * 70)
    
    assert ChatMode.NORMAL.value == "normal"
    assert ChatMode.CODE.value == "code"
    assert ChatMode.DEBUG.value == "debug"
    assert ChatMode.EXPLAIN.value == "explain"
    assert ChatMode.REFACTOR.value == "refactor"
    assert ChatMode.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(ChatMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: ChatMode enum")
    print("=" * 70)


def test_message_dataclass():
    """
    Test: Message dataclass.
    """
    print("=" * 70)
    print("TEST: Message Dataclass")
    print("=" * 70)
    
    message = Message(
        id="msg_1",
        type=MessageType.USER,
        content="Hello",
        timestamp=datetime.now()
    )
    
    assert message.id == "msg_1", "ID eşleşmeli"
    assert message.type == MessageType.USER, "Type eşleşmeli"
    assert message.content == "Hello", "Content eşleşmeli"
    
    print(f"  ID: {message.id}")
    print(f"  Type: {message.type.value}")
    print(f"  Content: {message.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Message dataclass")
    print("=" * 70)


def test_chat_session_dataclass():
    """
    Test: ChatSession dataclass.
    """
    print("=" * 70)
    print("TEST: ChatSession Dataclass")
    print("=" * 70)
    
    now = datetime.now()
    session = ChatSession(
        id="session_1",
        title="Test Chat",
        created_at=now,
        updated_at=now
    )
    
    assert session.id == "session_1", "ID eşleşmeli"
    assert session.title == "Test Chat", "Title eşleşmeli"
    assert session.is_active == True, "Active olmalı"
    
    print(f"  ID: {session.id}")
    print(f"  Title: {session.title}")
    print(f"  Active: {session.is_active}")
    
    print("\n" + "=" * 70)
    print("PASS: ChatSession dataclass")
    print("=" * 70)


def test_chat_interface_config_dataclass():
    """
    Test: ChatInterfaceConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ChatInterfaceConfig Dataclass")
    print("=" * 70)
    
    config = ChatInterfaceConfig(
        enabled=True,
        show_timestamps=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_timestamps == True, "Show timestamps eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show timestamps: {config.show_timestamps}")
    
    print("\n" + "=" * 70)
    print("PASS: ChatInterfaceConfig dataclass")
    print("=" * 70)


def test_chat_interface_result_dataclass():
    """
    Test: ChatInterfaceResult dataclass.
    """
    print("=" * 70)
    print("TEST: ChatInterfaceResult Dataclass")
    print("=" * 70)
    
    result = ChatInterfaceResult(success=True)
    result.message_text = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message_text == "Test message", "Message text eşleşmeli"
    assert isinstance(result.messages, list), "Messages list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message text: {result.message_text}")
    print(f"  Messages: {len(result.messages)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ChatInterfaceResult dataclass")
    print("=" * 70)


def test_chat_interface_manager_initialization():
    """
    Test: ChatInterfaceManager initialization.
    """
    print("=" * 70)
    print("TEST: ChatInterfaceManager Initialization")
    print("=" * 70)
    
    config = ChatInterfaceConfig()
    manager = ChatInterfaceManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.sessions) == 0, "Sessions boş olmalı"
    assert manager.active_session_id is None, "Active session None olmalı"
    
    print(f"  Sessions: {len(manager.sessions)}")
    print(f"  Active session: {manager.active_session_id}")
    
    print("\n" + "=" * 70)
    print("PASS: ChatInterfaceManager initialization")
    print("=" * 70)


def test_create_session():
    """
    Test: Create session.
    """
    print("=" * 70)
    print("TEST: Create Session")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    result = manager.create_session("Test Chat")
    
    assert result.success == True, "Oluşturma başarılı olmalı"
    assert result.session is not None, "Session olmalı"
    assert len(manager.sessions) > 0, "Session eklenmeli"
    
    print(f"  Session created: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Create session")
    print("=" * 70)


def test_delete_session():
    """
    Test: Delete session.
    """
    print("=" * 70)
    print("TEST: Delete Session")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    result = manager.create_session("Test Chat")
    session_id = result.session.id
    
    result = manager.delete_session(session_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert session_id not in manager.sessions, "Session silinmeli"
    
    print(f"  Session deleted: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete session")
    print("=" * 70)


def test_get_session():
    """
    Test: Get session.
    """
    print("=" * 70)
    print("TEST: Get Session")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    result = manager.create_session("Test Chat")
    session_id = result.session.id
    
    retrieved_session = manager.get_session(session_id)
    
    assert retrieved_session is not None, "Session bulunmalı"
    assert retrieved_session.id == session_id, "ID eşleşmeli"
    
    print(f"  Session: {retrieved_session.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get session")
    print("=" * 70)


def test_get_all_sessions():
    """
    Test: Get all sessions.
    """
    print("=" * 70)
    print("TEST: Get All Sessions")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat 1")
    manager.create_session("Test Chat 2")
    
    sessions = manager.get_all_sessions()
    
    assert len(sessions) == 2, "2 session olmalı"
    
    print(f"  Total sessions: {len(sessions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all sessions")
    print("=" * 70)


def test_set_active_session():
    """
    Test: Set active session.
    """
    print("=" * 70)
    print("TEST: Set Active Session")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    result = manager.create_session("Test Chat")
    session_id = result.session.id
    
    result = manager.set_active_session(session_id)
    
    assert result.success == True, "Set başarılı olmalı"
    assert manager.active_session_id == session_id, "Active session eşleşmeli"
    
    print(f"  Active session set: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Set active session")
    print("=" * 70)


def test_add_message():
    """
    Test: Add message.
    """
    print("=" * 70)
    print("TEST: Add Message")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    
    result = manager.add_message("Hello!", MessageType.USER)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.message is not None, "Message olmalı"
    
    print(f"  Message added: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Add message")
    print("=" * 70)


def test_edit_message():
    """
    Test: Edit message.
    """
    print("=" * 70)
    print("TEST: Edit Message")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    result = manager.add_message("Hello!", MessageType.USER)
    message_id = result.message.id
    
    result = manager.edit_message(message_id, "Hello World!")
    
    assert result.success == True, "Edit başarılı olmalı"
    
    print(f"  Message edited: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Edit message")
    print("=" * 70)


def test_delete_message():
    """
    Test: Delete message.
    """
    print("=" * 70)
    print("TEST: Delete Message")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    result = manager.add_message("Hello!", MessageType.USER)
    message_id = result.message.id
    
    result = manager.delete_message(message_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    
    print(f"  Message deleted: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Delete message")
    print("=" * 70)


def test_reply_to_message():
    """
    Test: Reply to message.
    """
    print("=" * 70)
    print("TEST: Reply to Message")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    result = manager.add_message("Hello!", MessageType.USER)
    message_id = result.message.id
    
    result = manager.reply_to_message(message_id, "Hi there!")
    
    assert result.success == True, "Reply başarılı olmalı"
    
    print(f"  Reply added: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Reply to message")
    print("=" * 70)


def test_get_messages():
    """
    Test: Get messages.
    """
    print("=" * 70)
    print("TEST: Get Messages")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    manager.add_message("Hello!", MessageType.USER)
    
    messages = manager.get_messages()
    
    assert len(messages) > 0, "Messages olmalı"
    
    print(f"  Total messages: {len(messages)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get messages")
    print("=" * 70)


def test_search_messages():
    """
    Test: Search messages.
    """
    print("=" * 70)
    print("TEST: Search Messages")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    manager.add_message("Hello World!", MessageType.USER)
    
    messages = manager.search_messages("Hello")
    
    assert len(messages) > 0, "Arama sonucu olmalı"
    
    print(f"  Search results: {len(messages)}")
    
    print("\n" + "=" * 70)
    print("PASS: Search messages")
    print("=" * 70)


def test_get_messages_by_type():
    """
    Test: Get messages by type.
    """
    print("=" * 70)
    print("TEST: Get Messages by Type")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    manager.add_message("Hello!", MessageType.USER)
    
    messages = manager.get_messages_by_type(MessageType.USER)
    
    assert len(messages) > 0, "User messages olmalı"
    
    print(f"  User messages: {len(messages)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get messages by type")
    print("=" * 70)


def test_clear_session_messages():
    """
    Test: Clear session messages.
    """
    print("=" * 70)
    print("TEST: Clear Session Messages")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    manager.create_session("Test Chat")
    manager.add_message("Hello!", MessageType.USER)
    
    result = manager.clear_session_messages()
    
    assert result.success == True, "Clear başarılı olmalı"
    
    messages = manager.get_messages()
    assert len(messages) == 0, "Messages temizlenmeli"
    
    print(f"  Messages cleared: {result.message_text}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear session messages")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = ChatInterfaceManager()
    
    new_config = ChatInterfaceConfig(max_messages=2000)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_messages == 2000, "Config güncellenmeli"
    
    print(f"  Max messages: {manager.config.max_messages}")
    
    print("\n" + "=" * 70)
    print("PASS: Update config")
    print("=" * 70)


def test_get_config():
    """
    Test: Get config.
    """
    print("=" * 70)
    print("TEST: Get Config")
    print("=" * 70)
    
    config = ChatInterfaceConfig(max_messages=2000)
    manager = ChatInterfaceManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_messages == 2000, "Config eşleşmeli"
    
    print(f"  Max messages: {retrieved_config.max_messages}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_message_type_enum()
        test2 = test_message_status_enum()
        test3 = test_chat_mode_enum()
        test4 = test_message_dataclass()
        test5 = test_chat_session_dataclass()
        test6 = test_chat_interface_config_dataclass()
        test7 = test_chat_interface_result_dataclass()
        test8 = test_chat_interface_manager_initialization()
        test9 = test_create_session()
        test10 = test_delete_session()
        test11 = test_get_session()
        test12 = test_get_all_sessions()
        test13 = test_set_active_session()
        test14 = test_add_message()
        test15 = test_edit_message()
        test16 = test_delete_message()
        test17 = test_reply_to_message()
        test18 = test_get_messages()
        test19 = test_search_messages()
        test20 = test_get_messages_by_type()
        test21 = test_clear_session_messages()
        test22 = test_update_config()
        test23 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"MessageType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"MessageStatus Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ChatMode Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Message Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ChatSession Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ChatInterfaceConfig Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"ChatInterfaceResult Dataclass: {'PASS' if test7 else 'FAIL'}")
        print(f"ChatInterfaceManager Initialization: {'PASS' if test8 else 'FAIL'}")
        print(f"Create Session: {'PASS' if test9 else 'FAIL'}")
        print(f"Delete Session: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Session: {'PASS' if test11 else 'FAIL'}")
        print(f"Get All Sessions: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Active Session: {'PASS' if test13 else 'FAIL'}")
        print(f"Add Message: {'PASS' if test14 else 'FAIL'}")
        print(f"Edit Message: {'PASS' if test15 else 'FAIL'}")
        print(f"Delete Message: {'PASS' if test16 else 'FAIL'}")
        print(f"Reply to Message: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Messages: {'PASS' if test18 else 'FAIL'}")
        print(f"Search Messages: {'PASS' if test19 else 'FAIL'}")
        print(f"Get Messages by Type: {'PASS' if test20 else 'FAIL'}")
        print(f"Clear Session Messages: {'PASS' if test21 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test22 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test23 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22, test23])
        print(f"\nTOPLAM: {'PASS' if all_passed else 'FAIL'}")
        print("=" * 70)
        
        sys.exit(0 if all_passed else 1)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
