"""
Quality Test: Minimap
Minimap system testleri.
"""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from app.editor.minimap import (
    MinimapEngine,
    MinimapPosition,
    MinimapSize,
    RenderMode,
    MinimapRegion,
    MinimapViewport,
    MinimapConfig,
    MinimapRenderResult
)


def test_render_minimap():
    """
    Test: Render minimap.
    """
    print("=" * 70)
    print("TEST: Render Minimap")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    code = """def my_function():
    x = 10
    return x
"""
    
    result = engine.render_minimap(code, current_line=0)
    
    assert result.success, "Render başarılı olmalı"
    assert len(result.rendered_lines) > 0, "Satırlar render edilmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Rendered lines: {len(result.rendered_lines)}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Render minimap")
    print("=" * 70)


def test_update_viewport():
    """
    Test: Update viewport.
    """
    print("=" * 70)
    print("TEST: Update Viewport")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    result = engine.update_viewport(0, 10, 100)
    
    assert result.success, "Update başarılı olmalı"
    assert result.viewport is not None, "Viewport olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Viewport: {result.viewport.start_line}-{result.viewport.end_line}")
    
    print("\n" + "=" * 70)
    print("PASS: Update viewport")
    print("=" * 70)


def test_add_region():
    """
    Test: Add region.
    """
    print("=" * 70)
    print("TEST: Add Region")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    result = engine.add_region(0, 5, color="#ff0000", highlight=True)
    
    assert result.success, "Ekleme başarılı olmalı"
    assert len(result.regions) > 0, "Region eklenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Regions: {len(result.regions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Add region")
    print("=" * 70)


def test_remove_region():
    """
    Test: Remove region.
    """
    print("=" * 70)
    print("TEST: Remove Region")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    # Region ekle
    engine.add_region(0, 5)
    
    # Kaldır
    result = engine.remove_region(0)
    
    assert result.success, "Kaldırma başarılı olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Remove region")
    print("=" * 70)


def test_clear_regions():
    """
    Test: Clear regions.
    """
    print("=" * 70)
    print("TEST: Clear Regions")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    # Region'lar ekle
    engine.add_region(0, 5)
    engine.add_region(10, 15)
    
    # Temizle
    result = engine.clear_regions()
    
    assert result.success, "Temizleme başarılı olmalı"
    assert len(result.regions) == 0, "Region'lar temizlenmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Regions: {len(result.regions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Clear regions")
    print("=" * 70)


def test_get_regions():
    """
    Test: Get regions.
    """
    print("=" * 70)
    print("TEST: Get Regions")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    # Region ekle
    engine.add_region(0, 5)
    
    regions = engine.get_regions()
    
    assert len(regions) > 0, "Region'lar olmalı"
    
    print(f"  Regions: {len(regions)}")
    
    print("\n" + "=" * 70)
    print("PASS: Get regions")
    print("=" * 70)


def test_update_config():
    """
    Test: Update config.
    """
    print("=" * 70)
    print("TEST: Update Config")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    new_config = MinimapConfig(enabled=False)
    result = engine.update_config(new_config)
    
    assert result.success, "Güncelleme başarılı olmalı"
    
    print(f"  Success: {result.success}")
    
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
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    retrieved_config = engine.get_config()
    
    assert retrieved_config is not None, "Config olmalı"
    assert retrieved_config.enabled == True, "Config eşleşmeli"
    
    print(f"  Enabled: {retrieved_config.enabled}")
    
    print("\n" + "=" * 70)
    print("PASS: Get config")
    print("=" * 70)


def test_toggle_minimap():
    """
    Test: Toggle minimap.
    """
    print("=" * 70)
    print("TEST: Toggle Minimap")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    result = engine.toggle_minimap()
    
    assert result.success, "Toggle başarılı olmalı"
    assert engine.config.enabled == False, "Disabled olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    
    print("\n" + "=" * 70)
    print("PASS: Toggle minimap")
    print("=" * 70)


def test_set_position():
    """
    Test: Set position.
    """
    print("=" * 70)
    print("TEST: Set Position")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    result = engine.set_position(MinimapPosition.LEFT)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.position == MinimapPosition.LEFT, "Position eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Position: {engine.config.position.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set position")
    print("=" * 70)


def test_set_size():
    """
    Test: Set size.
    """
    print("=" * 70)
    print("TEST: Set Size")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    result = engine.set_size(MinimapSize.LARGE)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.size == MinimapSize.LARGE, "Size eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Size: {engine.config.size.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set size")
    print("=" * 70)


def test_set_opacity():
    """
    Test: Set opacity.
    """
    print("=" * 70)
    print("TEST: Set Opacity")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    result = engine.set_opacity(0.5)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.opacity == 0.5, "Opacity eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Opacity: {engine.config.opacity}")
    
    print("\n" + "=" * 70)
    print("PASS: Set opacity")
    print("=" * 70)


def test_set_render_mode():
    """
    Test: Set render mode.
    """
    print("=" * 70)
    print("TEST: Set Render Mode")
    print("=" * 70)
    
    config = MinimapConfig()
    engine = MinimapEngine(config)
    
    result = engine.set_render_mode(RenderMode.BLOCKS)
    
    assert result.success, "Ayar başarılı olmalı"
    assert engine.config.render_mode == RenderMode.BLOCKS, "Mode eşleşmeli"
    
    print(f"  Success: {result.success}")
    print(f"  Mode: {engine.config.render_mode.value}")
    
    print("\n" + "=" * 70)
    print("PASS: Set render mode")
    print("=" * 70)


def test_minimap_position_enum():
    """
    Test: MinimapPosition enum.
    """
    print("=" * 70)
    print("TEST: MinimapPosition Enum")
    print("=" * 70)
    
    assert MinimapPosition.RIGHT.value == "right"
    assert MinimapPosition.LEFT.value == "left"
    
    print(f"  All enum values verified")
    print(f"  Total positions: {len(MinimapPosition)}")
    
    print("\n" + "=" * 70)
    print("PASS: MinimapPosition enum")
    print("=" * 70)


def test_minimap_size_enum():
    """
    Test: MinimapSize enum.
    """
    print("=" * 70)
    print("TEST: MinimapSize Enum")
    print("=" * 70)
    
    assert MinimapSize.SMALL.value == "small"
    assert MinimapSize.MEDIUM.value == "medium"
    assert MinimapSize.LARGE.value == "large"
    assert MinimapSize.AUTO.value == "auto"
    
    print(f"  All enum values verified")
    print(f"  Total sizes: {len(MinimapSize)}")
    
    print("\n" + "=" * 70)
    print("PASS: MinimapSize enum")
    print("=" * 70)


def test_render_mode_enum():
    """
    Test: RenderMode enum.
    """
    print("=" * 70)
    print("TEST: RenderMode Enum")
    print("=" * 70)
    
    assert RenderMode.TEXT.value == "text"
    assert RenderMode.BLOCKS.value == "blocks"
    assert RenderMode.OUTLINE.value == "outline"
    
    print(f"  All enum values verified")
    print(f"  Total modes: {len(RenderMode)}")
    
    print("\n" + "=" * 70)
    print("PASS: RenderMode enum")
    print("=" * 70)


def test_minimap_region_dataclass():
    """
    Test: MinimapRegion dataclass.
    """
    print("=" * 70)
    print("TEST: MinimapRegion Dataclass")
    print("=" * 70)
    
    region = MinimapRegion(
        start_line=0,
        end_line=5,
        color="#ff0000",
        highlight=True
    )
    
    assert region.start_line == 0, "Start line eşleşmeli"
    assert region.end_line == 5, "End line eşleşmeli"
    assert region.color == "#ff0000", "Color eşleşmeli"
    
    print(f"  Start line: {region.start_line}")
    print(f"  End line: {region.end_line}")
    print(f"  Color: {region.color}")
    
    print("\n" + "=" * 70)
    print("PASS: MinimapRegion dataclass")
    print("=" * 70)


def test_minimap_viewport_dataclass():
    """
    Test: MinimapViewport dataclass.
    """
    print("=" * 70)
    print("TEST: MinimapViewport Dataclass")
    print("=" * 70)
    
    viewport = MinimapViewport(
        start_line=0,
        end_line=10,
        visible_ratio=0.1
    )
    
    assert viewport.start_line == 0, "Start line eşleşmeli"
    assert viewport.end_line == 10, "End line eşleşmeli"
    assert viewport.visible_ratio == 0.1, "Ratio eşleşmeli"
    
    print(f"  Start line: {viewport.start_line}")
    print(f"  End line: {viewport.end_line}")
    print(f"  Visible ratio: {viewport.visible_ratio}")
    
    print("\n" + "=" * 70)
    print("PASS: MinimapViewport dataclass")
    print("=" * 70)


def test_minimap_config_dataclass():
    """
    Test: MinimapConfig dataclass.
    """
    print("=" * 70)
    print("TEST: MinimapConfig Dataclass")
    print("=" * 70)
    
    config = MinimapConfig(
        enabled=True,
        position=MinimapPosition.RIGHT,
        size=MinimapSize.AUTO
    )
    
    assert config.enabled == True, "Enabled eşleşmeli"
    assert config.position == MinimapPosition.RIGHT, "Position eşleşmeli"
    assert config.size == MinimapSize.AUTO, "Size eşleşmeli"
    
    print(f"  Enabled: {config.enabled}")
    print(f"  Position: {config.position.value}")
    print(f"  Size: {config.size.value}")
    
    print("\n" + "=" * 70)
    print("PASS: MinimapConfig dataclass")
    print("=" * 70)


def test_minimap_render_result_dataclass():
    """
    Test: MinimapRenderResult dataclass.
    """
    print("=" * 70)
    print("TEST: MinimapRenderResult Dataclass")
    print("=" * 70)
    
    result = MinimapRenderResult(success=True)
    result.message = "Test message"
    
    assert result.success == True, "Success eşleşmeli"
    assert result.message == "Test message", "Message eşleşmeli"
    assert isinstance(result.rendered_lines, list), "Rendered lines list olmalı"
    assert isinstance(result.regions, list), "Regions list olmalı"
    
    print(f"  Success: {result.success}")
    print(f"  Message: {result.message}")
    print(f"  Rendered lines: {len(result.rendered_lines)}")
    print(f"  Regions: {len(result.regions)}")
    
    print("\n" + "=" * 70)
    print("PASS: MinimapRenderResult dataclass")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_render_minimap()
        test2 = test_update_viewport()
        test3 = test_add_region()
        test4 = test_remove_region()
        test5 = test_clear_regions()
        test6 = test_get_regions()
        test7 = test_update_config()
        test8 = test_get_config()
        test9 = test_toggle_minimap()
        test10 = test_set_position()
        test11 = test_set_size()
        test12 = test_set_opacity()
        test13 = test_set_render_mode()
        test14 = test_minimap_position_enum()
        test15 = test_minimap_size_enum()
        test16 = test_render_mode_enum()
        test17 = test_minimap_region_dataclass()
        test18 = test_minimap_viewport_dataclass()
        test19 = test_minimap_config_dataclass()
        test20 = test_minimap_render_result_dataclass()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Render Minimap: {'PASS' if test1 else 'FAIL'}")
        print(f"Update Viewport: {'PASS' if test2 else 'FAIL'}")
        print(f"Add Region: {'PASS' if test3 else 'FAIL'}")
        print(f"Remove Region: {'PASS' if test4 else 'FAIL'}")
        print(f"Clear Regions: {'PASS' if test5 else 'FAIL'}")
        print(f"Get Regions: {'PASS' if test6 else 'FAIL'}")
        print(f"Update Config: {'PASS' if test7 else 'FAIL'}")
        print(f"Get Config: {'PASS' if test8 else 'FAIL'}")
        print(f"Toggle Minimap: {'PASS' if test9 else 'FAIL'}")
        print(f"Set Position: {'PASS' if test10 else 'FAIL'}")
        print(f"Set Size: {'PASS' if test11 else 'FAIL'}")
        print(f"Set Opacity: {'PASS' if test12 else 'FAIL'}")
        print(f"Set Render Mode: {'PASS' if test13 else 'FAIL'}")
        print(f"MinimapPosition Enum: {'PASS' if test14 else 'FAIL'}")
        print(f"MinimapSize Enum: {'PASS' if test15 else 'FAIL'}")
        print(f"RenderMode Enum: {'PASS' if test16 else 'FAIL'}")
        print(f"MinimapRegion Dataclass: {'PASS' if test17 else 'FAIL'}")
        print(f"MinimapViewport Dataclass: {'PASS' if test18 else 'FAIL'}")
        print(f"MinimapConfig Dataclass: {'PASS' if test19 else 'FAIL'}")
        print(f"MinimapRenderResult Dataclass: {'PASS' if test20 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9, test10, test11, test12, test13, test14, test15, test16, test17, test18, test19, test20])
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
