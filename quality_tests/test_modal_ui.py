"""
Quality Test: Modal UI
Modal UI system testleri for UI module.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.ui.modal_ui import (
    ModalType,
    ModalSize,
    ModalPosition,
    Modal,
    ModalConfig,
    ModalResult,
    ModalUIManager
)


def test_modal_type_enum():
    """
    Test: ModalType enum.
    """
    print("=" * 70)
    print("TEST: ModalType Enum")
    print("=" * 70)
    
    assert ModalType.ALERT.value == "alert"
    assert ModalType.CONFIRM.value == "confirm"
    assert ModalType.PROMPT.value == "prompt"
    assert ModalType.INFO.value == "info"
    assert ModalType.SUCCESS.value == "success"
    assert ModalType.WARNING.value == "warning"
    assert ModalType.ERROR.value == "error"
    assert ModalType.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total types: {len(ModalType)}")
    
    print("\n" + "=" * 70)
    print("PASS: ModalType enum")
    print("=" * 70)


def test_modal_size_enum():
    """
    Test: ModalSize enum.
    """
    print("=" * 70)
    print("TEST: ModalSize Enum")
    print("=" * 70)
    
    assert ModalSize.SMALL.value == "small"
    assert ModalSize.MEDIUM.value == "medium"
    assert ModalSize.LARGE.value == "large"
    assert ModalSize.EXTRA_LARGE.value == "extra_large"
    assert ModalSize.FULLSCREEN.value == "fullscreen"
    assert ModalSize.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total sizes: {len(ModalSize)}")
    
    print("\n" + "=" * 70)
    print("PASS: ModalSize enum")
    print("=" * 70)


def test_modal_position_enum():
    """
    Test: ModalPosition enum.
    """
    print("=" * 70)
    print("TEST: ModalPosition Enum")
    print("=" * 70)
    
    assert ModalPosition.CENTER.value == "center"
    assert ModalPosition.TOP.value == "top"
    assert ModalPosition.BOTTOM.value == "bottom"
    assert ModalPosition.LEFT.value == "left"
    assert ModalPosition.RIGHT.value == "right"
    assert ModalPosition.CUSTOM.value == "custom"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(ModalPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: ModalPosition enum")
    print("=" * 70)


def test_modal_dataclass():
    """
    Test: Modal dataclass.
    """
    print("=" * 70)
    print("TEST: Modal Dataclass")
    print("=" * 70)
    
    modal = Modal(
        id="modal_1",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    assert modal.id == "modal_1", "ID eşleşmeli"
    assert modal.type == ModalType.INFO, "Type eşleşmeli"
    assert modal.title == "Info", "Title eşleşmeli"
    assert modal.content == "This is an info modal", "Content eşleşmeli"
    
    print(f"  ID: {modal.id}")
    print(f"  Type: {modal.type.value}")
    print(f"  Title: {modal.title}")
    print(f"  Content: {modal.content}")
    
    print("\n" + "=" * 70)
    print("PASS: Modal dataclass")
    print("=" * 70)


def test_modal_config_dataclass():
    """
    Test: ModalConfig dataclass.
    """
    print("=" * 70)
    print("TEST: ModalConfig Dataclass")
    print("=" * 70)
    
    config = ModalConfig(
        enabled=True,
        show_overlay=True
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.show_overlay == True, "Show overlay eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Show overlay: {config.show_overlay}")
    
    print("\n" + "=" * 70)
    print("PASS: ModalConfig dataclass")
    print("=" * 70)


def test_modal_result_dataclass():
    """
    Test: ModalResult dataclass.
    """
    print("=" * 70)
    print("TEST: ModalResult Dataclass")
    print("=" * 70)
    
    result = ModalResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.modals, list), "Modals list olmalı"
    assert isinstance(result.errors, list), "Errors list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Modals: {len(result.modals)}")
    print(f"  Errors: {len(result.errors)}")
    
    print("\n" + "=" * 70)
    print("PASS: ModalResult dataclass")
    print("=" * 70)


def test_modal_ui_manager_initialization():
    """
    Test: ModalUIManager initialization.
    """
    print("=" * 70)
    print("TEST: ModalUIManager Initialization")
    print("=" * 70)
    
    config = ModalConfig()
    manager = ModalUIManager(config)
    
    assert manager.config == config, "Config eşleşmeli"
    assert len(manager.modals) == 0, "Modals boş olmalı"
    assert len(manager.modal_stack) == 0, "Modal stack boş olmalı"
    
    print(f"  Modals: {len(manager.modals)}")
    print(f"  Modal stack: {len(manager.modal_stack)}")
    
    print("\n" + "=" * 70)
    print("PASS: ModalUIManager initialization")
    print("=" * 70)


def test_add_modal():
    """
    Test: Add modal.
    """
    print("=" * 70)
    print("TEST: Add Modal")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    
    assert result.success == True, "Ekleme başarılı olmalı"
    assert result.modal is not None, "Modal olmalı"
    assert len(manager.modals) > 0, "Modal eklenmeli"
    
    print(f"  Modal added: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Add modal")
    print("=" * 70)


def test_remove_modal():
    """
    Test: Remove modal.
    """
    print("=" * 70)
    print("TEST: Remove Modal")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    result = manager.remove_modal(modal_id)
    
    assert result.success == True, "Silme başarılı olmalı"
    assert modal_id not in manager.modals, "Modal silinmeli"
    
    print(f"  Modal removed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove modal")
    print("=" * 70)


def test_get_modal():
    """
    Test: Get modal.
    """
    print("=" * 70)
    print("TEST: Get Modal")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    retrieved_modal = manager.get_modal(modal_id)
    
    assert retrieved_modal is not None, "Modal bulunmalı"
    assert retrieved_modal.id == modal_id, "ID eşleşmeli"
    
    print(f"  Modal: {retrieved_modal.title}")
    
    print("\n" + "=" * 70)
    print("PASS: Get modal")
    print("=" * 70)


def test_get_all_modals():
    """
    Test: Get all modals.
    """
    print("=" * 70)
    print("TEST: Get All Modals")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    manager.add_modal(modal)
    modals = manager.get_all_modals()
    
    assert len(modals) > 0, "Modals olmalı"
    
    print(f"  Total modals: {len(modals)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get all modals")
    print("=" * 70)


def test_get_open_modals():
    """
    Test: Get open modals.
    """
    print("=" * 70)
    print("TEST: Get Open Modals")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    manager.open_modal(result.modal.id)
    
    open_modals = manager.get_open_modals()
    
    assert len(open_modals) > 0, "Open modals olmalı"
    
    print(f"  Open modals: {len(open_modals)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get open modals")
    print("=" * 70)


def test_open_modal():
    """
    Test: Open modal.
    """
    print("=" * 70)
    print("TEST: Open Modal")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    result = manager.open_modal(modal_id)
    
    assert result.success == True, "Open başarılı olmalı"
    
    print(f"  Modal opened: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Open modal")
    print("=" * 70)


def test_close_modal():
    """
    Test: Close modal.
    """
    print("=" * 70)
    print("TEST: Close Modal")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    manager.open_modal(modal_id)
    result = manager.close_modal(modal_id)
    
    assert result.success == True, "Close başarılı olmalı"
    
    print(f"  Modal closed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close modal")
    print("=" * 70)


def test_confirm_modal():
    """
    Test: Confirm modal.
    """
    print("=" * 70)
    print("TEST: Confirm Modal")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.CONFIRM,
        title="Confirm",
        content="Are you sure?"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    manager.open_modal(modal_id)
    result = manager.confirm_modal(modal_id)
    
    assert result.success == True, "Confirm başarılı olmalı"
    
    print(f"  Modal confirmed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Confirm modal")
    print("=" * 70)


def test_cancel_modal():
    """
    Test: Cancel modal.
    """
    print("=" * 70)
    print("TEST: Cancel Modal")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.CONFIRM,
        title="Confirm",
        content="Are you sure?"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    manager.open_modal(modal_id)
    result = manager.cancel_modal(modal_id)
    
    assert result.success == True, "Cancel başarılı olmalı"
    
    print(f"  Modal cancelled: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Cancel modal")
    print("=" * 70)


def test_set_modal_size():
    """
    Test: Set modal size.
    """
    print("=" * 70)
    print("TEST: Set Modal Size")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    result = manager.set_modal_size(modal_id, ModalSize.LARGE)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Modal size set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set modal size")
    print("=" * 70)


def test_set_modal_position():
    """
    Test: Set modal position.
    """
    print("=" * 70)
    print("TEST: Set Modal Position")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    modal_id = result.modal.id
    
    result = manager.set_modal_position(modal_id, ModalPosition.TOP)
    
    assert result.success == True, "Set başarılı olmalı"
    
    print(f"  Modal position set: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Set modal position")
    print("=" * 70)


def test_close_all_modals():
    """
    Test: Close all modals.
    """
    print("=" * 70)
    print("TEST: Close All Modals")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    result = manager.add_modal(modal)
    manager.open_modal(result.modal.id)
    
    result = manager.close_all_modals()
    
    assert result.success == True, "Close başarılı olmalı"
    
    open_modals = manager.get_open_modals()
    assert len(open_modals) == 0, "Tüm modallar kapanmalı"
    
    print(f"  All modals closed: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Close all modals")
    print("=" * 70)


def test_clear_all_modals():
    """
    Test: Clear all modals.
    """
    print("=" * 70)
    print("TEST: Clear All Modals")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    modal = Modal(
        id="",
        type=ModalType.INFO,
        title="Info",
        content="This is an info modal"
    )
    
    manager.add_modal(modal)
    result = manager.clear_all_modals()
    
    assert result.success == True, "Clear başarılı olmalı"
    assert len(manager.modals) == 0, "Modals temizlenmeli"
    
    print(f"  All modals cleared: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear all modals")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    manager = ModalUIManager()
    
    new_config = ModalConfig(max_modals=10)
    result = manager.update_config(new_config)
    
    assert result.success == True, "Update başarılı olmalı"
    assert manager.config.max_modals == 10, "Config güncellenmeli"
    
    print(f"  Max modals: {manager.config.max_modals}")
    
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
    
    config = ModalConfig(max_modals=10)
    manager = ModalUIManager(config)
    
    retrieved_config = manager.get_config()
    
    assert retrieved_config.max_modals == 10, "Config eşleşmeli"
    
    print(f"  Max modals: {retrieved_config.max_modals}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_modal_type_enum()
        test2 = test_modal_size_enum()
        test3 = test_modal_position_enum()
        test4 = test_modal_dataclass()
        test5 = test_modal_config_dataclass()
        test6 = test_modal_result_dataclass()
        test7 = test_modal_ui_manager_initialization()
        test8 = test_add_modal()
        test9 = test_remove_modal()
        test10 = test_get_modal()
        test11 = test_get_all_modal()
        test12 = test_get_open_modals()
        test13 = test_open_modal()
        test14 = test_close_modal()
        test15 = test_confirm_modal()
        test16 = test_cancel_modal()
        test17 = test_set_modal_size()
        test18 = test_set_modal_position()
        test19 = test_close_all_modals()
        test20 = test_clear_all_modals()
        test21 = test_update_config()
        test22 = test_get_config()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"ModalType Enum: {'PASS' if test1 else 'FAIL'}")
        print(f"ModalSize Enum: {'PASS' if test2 else 'FAIL'}")
        print(f"ModalPosition Enum: {'PASS' if test3 else 'FAIL'}")
        print(f"Modal Dataclass: {'PASS' if test4 else 'FAIL'}")
        print(f"ModalConfig Dataclass: {'PASS' if test5 else 'FAIL'}")
        print(f"ModalResult Dataclass: {'PASS' if test6 else 'FAIL'}")
        print(f"ModalUIManager Initialization: {'PASS' if test7 else 'FAIL'}")
        print(f"Add Modal: {'PASS' if test8 else 'FAIL'}")
        print(f"Remove Modal: {'PASS' if test9 else 'FAIL'}")
        print(f"Get Modal: {'PASS' if test10 else 'FAIL'}")
        print(f"Get All Modals: {'PASS' if test11 else 'FAIL'}")
        print(f"Get Open Modals: {'PASS' if test12 else 'FAIL'}")
        print(f"Open Modal: {'PASS' if test13 else 'FAIL'}")
        print(f"Close Modal: {'PASS' if test14 else 'FAIL'}")
        print(f"Confirm Modal: {'PASS' if test15 else 'FAIL'}")
        print(f"Cancel Modal: {'PASS' if test16 else 'FAIL'}")
        print(f"Set Modal Size: {'PASS' if test17 else 'FAIL'}")
        print(f"Set Modal Position: {'PASS' if test18 else 'FAIL'}")
        print(f"Close All Modals: {'PASS' if test19 else 'FAIL'}")
        print(f"Clear All Modals: {'PASS' if test20 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test21 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test22 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20, test21, test22])
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
