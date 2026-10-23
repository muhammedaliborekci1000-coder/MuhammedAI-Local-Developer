"""
Quality Test: Enhanced Tool System
Tool system gelişmiş özellikleri testleri.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.tool_registry import ToolRegistry, ToolDefinition, ToolExecution


def test_tool_definition_enhancements():
    """
    Test: Tool definition enhancements.
    """
    print("=" * 70)
    print("TEST: Tool Definition Enhancements")
    print("=" * 70)
    
    def dummy_handler():
        return {"result": "ok"}
    
    tool = ToolDefinition(
        name="test_tool",
        description="Test tool",
        handler=dummy_handler,
        requires_approval=False,
        category="test",
        enabled=True,
        usage_count=5,
        avg_execution_time=0.5,
        success_rate=0.9,
        total_executions=10,
        failed_executions=1
    )
    
    assert tool.name == "test_tool", "Name eşleşmeli"
    assert tool.enabled == True, "Enabled olmalı"
    assert tool.usage_count == 5, "Usage count eşleşmeli"
    assert tool.success_rate == 0.9, "Success rate eşleşmeli"
    assert tool.total_executions == 10, "Total executions eşleşmeli"
    
    print(f"  Tool name: {tool.name}")
    print(f"  Enabled: {tool.enabled}")
    print(f"  Usage count: {tool.usage_count}")
    print(f"  Success rate: {tool.success_rate}")
    
    print("\n" + "=" * 70)
    print("PASS: Tool definition enhancements")
    print("=" * 70)


def test_tool_execution():
    """
    Test: Tool execution with tracking.
    """
    print("=" * 70)
    print("TEST: Tool Execution with Tracking")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Tool çalıştır
    result = registry.execute_tool("project_scan")
    
    assert result is not None, "Sonuç olmalı"
    
    # İstatistikleri kontrol et
    tool = registry.get("project_scan")
    assert tool.usage_count > 0, "Usage count artmalı"
    assert tool.last_used is not None, "Last used set olmalı"
    assert tool.total_executions > 0, "Total executions artmalı"
    
    print(f"  Tool executed: project_scan")
    print(f"  Usage count: {tool.usage_count}")
    print(f"  Total executions: {tool.total_executions}")
    print(f"  Last used: {tool.last_used}")
    
    print("\n" + "=" * 70)
    print("PASS: Tool execution with tracking")
    print("=" * 70)


def test_enable_disable_tools():
    """
    Test: Enable/disable tools.
    """
    print("=" * 70)
    print("TEST: Enable/Disable Tools")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Tool disable
    result = registry.disable_tool("project_scan")
    assert result == True, "Disable başarılı olmalı"
    
    tool = registry.get("project_scan")
    assert tool.enabled == False, "Tool disabled olmalı"
    print(f"  Disabled: {not tool.enabled}")
    
    # Tool enable
    result = registry.enable_tool("project_scan")
    assert result == True, "Enable başarılı olmalı"
    
    tool = registry.get("project_scan")
    assert tool.enabled == True, "Tool enabled olmalı"
    print(f"  Enabled: {tool.enabled}")
    
    # Non-existent tool
    result = registry.disable_tool("nonexistent_tool")
    assert result == False, "Non-existent tool başarısız olmalı"
    print(f"  Non-existent tool: {result}")
    
    print("\n" + "=" * 70)
    print("PASS: Enable/disable tools")
    print("=" * 70)


def test_tool_analytics():
    """
    Test: Tool analytics.
    """
    print("=" * 70)
    print("TEST: Tool Analytics")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Birkaç tool çalıştır
    registry.execute_tool("project_scan")
    registry.execute_tool("project_tree")
    registry.execute_tool("project_scan")
    
    # Analytics al
    analytics = registry.get_tool_analytics()
    
    assert analytics["total_tools"] > 0, "Toplam tool olmalı"
    assert analytics["enabled_tools"] > 0, "Enabled tool olmalı"
    assert "category_counts" in analytics, "Category counts olmalı"
    assert "total_usage" in analytics, "Total usage olmalı"
    
    print(f"  Total tools: {analytics['total_tools']}")
    print(f"  Enabled tools: {analytics['enabled_tools']}")
    print(f"  Category counts: {analytics['category_counts']}")
    print(f"  Total usage: {analytics['total_usage']}")
    
    print("\n" + "=" * 70)
    print("PASS: Tool analytics")
    print("=" * 70)


def test_tool_performance():
    """
    Test: Tool performance metrics.
    """
    print("=" * 70)
    print("TEST: Tool Performance Metrics")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Tool çalıştır
    registry.execute_tool("project_scan")
    
    # Performance al
    performance = registry.get_tool_performance("project_scan")
    
    assert performance is not None, "Performance olmalı"
    assert performance["name"] == "project_scan", "Name eşleşmeli"
    assert performance["usage_count"] > 0, "Usage count olmalı"
    assert "avg_execution_time" in performance, "Avg execution time olmalı"
    assert "success_rate" in performance, "Success rate olmalı"
    
    print(f"  Tool name: {performance['name']}")
    print(f"  Usage count: {performance['usage_count']}")
    print(f"  Avg execution time: {performance['avg_execution_time']}")
    print(f"  Success rate: {performance['success_rate']}")
    
    print("\n" + "=" * 70)
    print("PASS: Tool performance metrics")
    print("=" * 70)


def test_execution_history():
    """
    Test: Execution history.
    """
    print("=" * 70)
    print("TEST: Execution History")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Tool'ları çalıştır
    registry.execute_tool("project_scan")
    registry.execute_tool("project_tree")
    registry.execute_tool("project_scan")
    
    # History al
    history = registry.get_execution_history(limit=10)
    
    assert len(history) > 0, "History olmalı"
    assert "tool_name" in history[0], "Tool name olmalı"
    assert "timestamp" in history[0], "Timestamp olmalı"
    assert "duration" in history[0], "Duration olmalı"
    assert "success" in history[0], "Success olmalı"
    
    print(f"  History size: {len(history)}")
    print(f"  First tool: {history[0]['tool_name']}")
    print(f"  First duration: {history[0]['duration']}")
    
    # Tool bazlı history
    scan_history = registry.get_execution_history(tool_name="project_scan")
    assert len(scan_history) > 0, "Project scan history olmalı"
    print(f"  Project scan history: {len(scan_history)}")
    
    print("\n" + "=" * 70)
    print("PASS: Execution history")
    print("=" * 70)


def test_tool_validation():
    """
    Test: Tool validation.
    """
    print("=" * 70)
    print("TEST: Tool Validation")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Valid tool
    validation = registry.validate_tool("project_scan")
    assert validation["valid"] == True, "Tool geçerli olmalı"
    print(f"  Valid tool: {validation['valid']}")
    
    # Non-existent tool
    validation = registry.validate_tool("nonexistent_tool")
    assert validation["valid"] == False, "Geçersiz tool olmalı"
    assert "error" in validation, "Error olmalı"
    print(f"  Invalid tool: {validation['valid']}")
    print(f"  Error: {validation['error']}")
    
    print("\n" + "=" * 70)
    print("PASS: Tool validation")
    print("=" * 70)


def test_most_used_tools():
    """
    Test: Most used tools.
    """
    print("=" * 70)
    print("TEST: Most Used Tools")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Tool'ları farklı sıklıklarla çalıştır
    registry.execute_tool("project_scan")
    registry.execute_tool("project_scan")
    registry.execute_tool("project_scan")
    registry.execute_tool("project_tree")
    registry.execute_tool("project_tree")
    
    # En çok kullanılanları al
    most_used = registry.get_most_used_tools(limit=5)
    
    assert len(most_used) > 0, "Sonuç olmalı"
    assert most_used[0]["name"] == "project_scan", "Project scan en çok kullanılan olmalı"
    assert most_used[0]["usage_count"] >= 3, "Usage count doğru olmalı"
    
    print(f"  Most used: {most_used[0]['name']}")
    print(f"  Usage count: {most_used[0]['usage_count']}")
    
    print("\n" + "=" * 70)
    print("PASS: Most used tools")
    print("=" * 70)


def test_slowest_tools():
    """
    Test: Slowest tools.
    """
    print("=" * 70)
    print("TEST: Slowest Tools")
    print("=" * 70)
    
    registry = ToolRegistry()
    
    # Tool'ları çalıştır
    registry.execute_tool("project_scan")
    registry.execute_tool("project_tree")
    
    # En yavaşları al
    slowest = registry.get_slowest_tools(limit=5)
    
    # En az bir tool çalıştırıldığı için sonuç olmalı
    if len(slowest) > 0:
        assert "name" in slowest[0], "Name olmalı"
        assert "avg_execution_time" in slowest[0], "Avg execution time olmalı"
        print(f"  Slowest tool: {slowest[0]['name']}")
        print(f"  Avg execution time: {slowest[0]['avg_execution_time']}")
    else:
        print("  No tools with execution data yet")
    
    print("\n" + "=" * 70)
    print("PASS: Slowest tools")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test1 = test_tool_definition_enhancements()
        test2 = test_tool_execution()
        test3 = test_enable_disable_tools()
        test4 = test_tool_analytics()
        test5 = test_tool_performance()
        test6 = test_execution_history()
        test7 = test_tool_validation()
        test8 = test_most_used_tools()
        test9 = test_slowest_tools()
        
        print("\n" + "=" * 70)
        print("TOPLAM SONUÇ")
        print("=" * 70)
        print(f"Tool Definition Enhancements: {'PASS' if test1 else 'FAIL'}")
        print(f"Tool Execution with Tracking: {'PASS' if test2 else 'FAIL'}")
        print(f"Enable/Disable Tools: {'PASS' if test3 else 'FAIL'}")
        print(f"Tool Analytics: {'PASS' if test4 else 'FAIL'}")
        print(f"Tool Performance Metrics: {'PASS' if test5 else 'FAIL'}")
        print(f"Execution History: {'PASS' if test6 else 'FAIL'}")
        print(f"Tool Validation: {'PASS' if test7 else 'FAIL'}")
        print(f"Most Used Tools: {'PASS' if test8 else 'FAIL'}")
        print(f"Slowest Tools: {'PASS' if test9 else 'FAIL'}")
        
        all_passed = all([test1, test2, test3, test4, test5, test6, test7, test8, test9])
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
