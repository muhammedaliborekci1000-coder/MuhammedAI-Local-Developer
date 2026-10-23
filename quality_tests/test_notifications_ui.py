"""
Quality Test: Notifications UI
Notifications UI system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.notifications_ui import (
    NotificationType,
    NotificationPriority,
    Notification,
    NotificationConfig,
    NotificationResult,
    NotificationsUIManager
)


def test_notification_type_enum():
    """
    Test: NotificationType enum.
    """
    print("=" * 70)
    print("TEST: NotificationType Enum")
    print("=" * 70)
    
    assert NotificationType.INFO.value == "info"
    assert NotificationType.WARNING.value == "warning"
    assert NotificationType.ERROR.value == "error"
    assert NotificationType.SUCCESS.value == "success"
    assert NotificationType.PROGRESS.value == "progress"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(NotificationType)}")
    
    print("\n" + "=" * 70)
    print("PASS: NotificationType enum")
    print("=" * 70)


def test_notification_priority_enum():
    """
    Test: NotificationPriority enum.
    """
    print("=" * 70)
    print("TEST: NotificationPriority Enum")
    print("=" * 70)
    
    assert NotificationPriority.LOW.value == "low"
    assert NotificationPriority.MEDIUM.value == "medium"
    assert NotificationPriority.HIGH.value == "high"
    assert NotificationPriority.URGENT.value == "urgent"
    
    print(f"  All enum values verified")
    print(f"  Total priorities: {len(NotificationPriority)}")
    
    print("\n" + "=" * 70)
    print("PASS: NotificationPriority enum")
    print("=" * 70)


def test_notification_dataclass():
    """
    Test: Notification dataclass.
    """
    print("=" * 70)
    print("TEST: Notification Dataclass")
    print("=" * 70)
    
    notification = Notification(
        id="notification_1",
        title="Test",
        message="Test message",
        type=NotificationType.INFO
    )
    
    assert notification.id == "notification_1", "ID eşleşmeli"
    assert notification.title == "Test", "Title eşleşmeli"
    assert notification.type == NotificationType.INFO, "Type eşleşmeli"
    
    print(f"  ID: {notification.id}")
    print(f"  Title: {notification.title}")
    print(f"  Type: {notification.type.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Notification dataclass")
    print("=" * 70)


def test_notification_config_dataclass():
    """
    Test: NotificationConfig dataclass.
    """
    print("=" * 70)
    print("TEST: NotificationConfig Dataclass")
    print("=" * 70)
    
    config = NotificationConfig(
        max_notifications=50,
        auto_dismiss=True
    )
    
    assert config.max_notifications == 50, "Max notifications eşleşmeli"
    assert config.auto_dismiss == True, "Auto dismiss eşleşmeli"
    
    print(f"  Max notifications: {config.max_notifications}")
    print(f"  Auto dismiss: {config.auto_dismiss}")
    
    print("\n" + "=" * 70)
    print("PASS: NotificationConfig dataclass")
    print("=" * 70)


def test_notification_result_dataclass():
    """
    Test: NotificationResult dataclass.
    """
    print("=" * 70)
    print("TEST: NotificationResult Dataclass")
    print("=" * 70)
    
    result = NotificationResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.notifications, list), "Notifications list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Notifications: {len(result.notifications)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: NotificationResult dataclass")
    print("=" * 70)


def test_notifications_ui_manager_initialization():
    """
    Test: NotificationsUIManager initialization.
    """
    print("=" * 70)
    print("TEST: NotificationsUIManager Initialization")
    print("=" * 70)
    
    config = NotificationConfig()
    manager = NotificationsUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.notifications) == 0, "Notifications boş olmalı"
    
    print(f"  Notifications: {len(manager.notifications)}")
    
    print("\n" + "=" * 70)
    print("PASS: NotificationsUIManager initialization")
    print("=" * 70)


def test_add_notification():
    """
    Test: Add notification.
    """
    print("=" * 70)
    print("TEST: Add Notification")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message",
        type=NotificationType.INFO
    )
    
    result = manager.add_notification(notification)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert len(manager.notifications) > 0, "Notification eklenmeli"
    
    print(f"  Notification added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add notification")
    print("=" * 70)


def test_remove_notification():
    """
    Test: Remove notification.
    """
    print("=" * 70)
    print("TEST: Remove Notification")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message"
    )
    
    result = manager.add_notification(notification)
    notification_id = result.notification.id
    
    result = manager.remove_notification(notification_id)
    
    assert result.success == True, "Kaldırma başarılı olmalı"
    assert notification_id not in manager.notifications, "Notification silinmeli"
    
    print(f"  Notification removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove notification")
    print("=" * 70)


def test_get_notification():
    """
    Test: Get notification.
    """
    print("=" * 70)
    print("TEST: Get Notification")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message"
    )
    
    result = manager.add_notification(notification)
    notification_id = result.notification.id
    
    retrieved_notification = manager.get_notification(notification_id)
    
    assert retrieved_notification is not None, "Notification bulunmalı"
    assert retrieved_notification.id == notification_id, "ID eşleşmeli"
    
    print(f"  Notification: {retrieved_notification.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get notification")
    print("=" * 70)


def test_get_all_notifications():
    """
    Test: Get all notifications.
    """
    print("=" * 70)
    print("TEST: Get All Notifications")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message"
    )
    
    manager.add_notification(notification)
    notifications = manager.get_all_notifications()
    
    assert len(notifications) > 0, "Notifications olmalı"
    
    print(f"  Total notifications: {len(notifications)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all notifications")
    print("=" * 70)


def test_get_notifications_by_type():
    """
    Test: Get notifications by type.
    """
    print("=" * 70)
    print("TEST: Get Notifications by Type")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message",
        type=NotificationType.INFO
    )
    
    manager.add_notification(notification)
    notifications = manager.get_notifications_by_type(NotificationType.INFO)
    
    assert len(notifications) > 0, "Info notifications olmalı"
    
    print(f"  Info notifications: {len(notifications)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get notifications by type")
    print("=" * 70)


def test_get_notifications_by_priority():
    """
    Test: Get notifications by priority.
    """
    print("=" * 70)
    print("TEST: Get Notifications by Priority")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message",
        priority=NotificationPriority.HIGH
    )
    
    manager.add_notification(notification)
    notifications = manager.get_notifications_by_priority(NotificationPriority.HIGH)
    
    assert len(notifications) > 0, "High priority notifications olmalı"
    
    print(f"  High priority notifications: {len(notifications)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get notifications by priority")
    print("=" * 70)


def test_get_unread_notifications():
    """
    Test: Get unread notifications.
    """
    print("=" * 70)
    print("TEST: Get Unread Notifications")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message",
        is_read=False
    )
    
    manager.add_notification(notification)
    unread = manager.get_unread_notifications()
    
    assert len(unread) > 0, "Unread notifications olmalı"
    
    print(f"  Unread notifications: {len(unread)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get unread notifications")
    print("=" * 70)


def test_mark_as_read():
    """
    Test: Mark as read.
    """
    print("=" * 70)
    print("TEST: Mark as Read")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message",
        is_read=False
    )
    
    result = manager.add_notification(notification)
    notification_id = result.notification.id
    
    result = manager.mark_as_read(notification_id)
    
    assert result.success == True, "Mark başarılı olmalı"
    assert result.notification.is_read == True, "Read olmalı"
    
    print(f"  Marked as read: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Mark as read")
    print("=" * 70)


def test_mark_all_as_read():
    """
    Test: Mark all as read.
    """
    print("=" * 70)
    print("TEST: Mark All as Read")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message",
        is_read=False
    )
    
    manager.add_notification(notification)
    result = manager.mark_all_as_read()
    
    assert result.success == True, "Mark all başarılı olmalı"
    
    print(f"  Marked all as read: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Mark all as read")
    print("=" * 70)


def test_clear_all_notifications():
    """
    Test: Clear all notifications.
    """
    print("=" * 70)
    print("TEST: Clear All Notifications")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message"
    )
    
    manager.add_notification(notification)
    result = manager.clear_all_notifications()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.notifications) == 0, "Notifications temizlenmeli"
    
    print(f"  Cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all notifications")
    print("=" * 70)


def test_update_notification():
    """
    Test: Update notification.
    """
    print("=" * 70)
    print("TEST: Update Notification")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message"
    )
    
    result = manager.add_notification(notification)
    notification_id = result.notification.id
    
    result = manager.update_notification(notification_id, title="Updated Title")
    
    assert result.success == True, "Update başarılı olmalı"
    assert result.notification.title == "Updated Title", "Title güncellenmeli"
    
    print(f"  Updated: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Update notification")
    print("=" * 70)


def test_get_notification_count():
    """
    Test: Get notification count.
    """
    print("=" * 70)
    print("TEST: Get Notification Count")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message"
    )
    
    manager.add_notification(notification)
    count = manager.get_notification_count()
    
    assert count > 0, "Count > 0 olmalı"
    
    print(f"  Count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get notification count")
    print("=" * 70)


def test_get_unread_count():
    """
    Test: Get unread count.
    """
    print("=" * 70)
    print("TEST: Get Unread Count")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    notification = Notification(
        id="",
        title="Test",
        message="Test message",
        is_read=False
    )
    
    manager.add_notification(notification)
    count = manager.get_unread_count()
    
    assert count > 0, "Unread count > 0 olmalı"
    
    print(f"  Unread count: {count}")
    
    print("\n" + "=" * 70)
    print("PASS: Get unread count")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = NotificationsUIManager()
    
    new_config = NotificationConfig(max_notifications=100)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_notifications == 100, "Config güncellenmeli"
    
    print(f"  Max notifications: {manager.config.max_notifications}")
    
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
    
    config = NotificationConfig(max_notifications=100)
    manager = NotificationsUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_notifications == 100, "Config eşleşmeli"
    
    print(f"  Max notifications: {retrieved_config.max_notifications}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_notification_type_enum()
        test2 = test_notification_priority_enum()
        test3 = test_notification_dataclass()
        test4 = test_notification_config_dataclass()
        test5 = test_notification_result_dataclass()
        test6 = test_notifications_ui_manager_initialization()
        test7 = test_add_notification()
        test8 = test_remove_notification()
        test9 = test_get_notification()
        test10 = test_get_all_notifications()
        test11 = test_get_notifications_by_type()
        test12 = test_get_notifications_by_priority()
        test13 = test_get_unread_notifications()
        test14 = test_mark_as_read()
        test15 = test_mark_all_as_read()
        test16 = test_clear_all_notifications()
        test17 = test_update_notification()
        test18 = test_get_notification_count()
        test19 = test_get_unread_count()
        test20 = test_update_config()
        test21 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"NotificationType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"NotificationPriority Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"Notification Dataclass: {'PASS' if test3 else 'FAIL'}")
        print(f"NotificationConfig Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"NotificationResult Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"NotificationsUIManager Initialization: {'PASS' if test6 else 'FAIL'}")
        print(f"Add Notification: {'PASS' if test7 else 'FAIL'}")
        print(f"Remove Notification: {'PASS' if test8 else 'FAIL'}")
        print(f"Get Notification: {'PASS' if test9 else 'FAIL'}")
        print(f"Get All Notifications: {'PASS' if test10 else 'FAIL'}")
        print(f"Get Notifications by Type: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Notifications by Priority: {'PASS' if test12 else 'FAIL'}")
        print(f"Get Unread Notifications: {'PASS' if test13 else 'FAIL'}")
        print(f"Mark as Read: {'PASS' if test14 else 'FAIL'}")
        print(f"Mark All as Read: {'PASS' if test15 else 'FAIL'}")
        print(f"Clear All Notifications: {'PASS' if test16 else 'FAIL'}")
        print(f"Update Notification: {'PASS' if test17 else 'FAIL'}")
        print(f"Get Notification Count: {'PASS' if test18 else 'FAIL'}")
        print(f"Get Unread Count: {'PASS' if test19 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test20 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test21 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21])
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
