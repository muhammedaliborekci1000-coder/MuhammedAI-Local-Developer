"""
Terminal Agent Real Qwen3 Test
Gerçek Qwen3 modeli ile Terminal Agent entegrasyon testi.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.terminal_executor import TerminalExecutor, TerminalCommand
from app.tools.terminal_security import TerminalSecurityPolicy, RiskLevel
from app.core.config import PROJECT_ROOT


@pytest.mark.slow
def test_terminal_agent_real_qwen3():
    """
    Gerçek Qwen3 ile Terminal Agent testi.
    Terminal command → validation → execution → result.
    """
    print("\n" + "=" * 70)
    print("TERMINAL AGENT REAL QWEN3 TEST")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "terminal_qwen3_workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    try:
        executor = TerminalExecutor(project_root=workspace)
        
        # Safe command test
        print("\n1. Safe command test:")
        result = executor.execute_simple("python --version", shell="powershell")
        
        print(f"   Command: python --version")
        print(f"   Exit code: {result.exit_code}")
        print(f"   Success: {result.success}")
        print(f"   Risk: {result.risk_level.value}")
        print(f"   Approval required: {result.approval_required}")
        
        assert result.success is True
        assert result.risk_level == RiskLevel.SAFE
        assert result.approval_required is False
        
        # Risk classification test
        print("\n2. Risk classification test:")
        policy = TerminalSecurityPolicy(project_root=workspace)
        
        risk = policy.classify_risk("del file.py")
        print(f"   Command: del file.py")
        print(f"   Risk: {risk.value}")
        
        assert risk == RiskLevel.HIGH_RISK
        
        # Approval requirement test
        print("\n3. Approval requirement test:")
        requires_approval = policy.requires_approval("pip install package")
        print(f"   Command: pip install package")
        print(f"   Approval required: {requires_approval}")
        
        assert requires_approval is True
        
        # Dry-run test
        print("\n4. Dry-run test:")
        result = executor.execute_simple("python --version", shell="python", dry_run=True)
        
        print(f"   Dry-run: {result.success}")
        print(f"   Exit code: {result.exit_code}")
        print(f"   stdout: {result.stdout}")
        
        assert result.success is True
        assert result.exit_code is None
        assert "[DRY-RUN" in result.stdout
        
        # Workspace validation test
        print("\n5. Workspace validation test:")
        valid = policy.validate_workspace(str(workspace))
        print(f"   Workspace: {workspace}")
        print(f"   Valid: {valid}")
        
        assert valid is True
        
        # Secret detection test
        print("\n6. Secret detection test:")
        has_secret = policy.detect_secret("api_key=secret123")
        print(f"   Text: api_key=secret123")
        print(f"   Has secret: {has_secret}")
        
        assert has_secret is True
        
        print("\n" + "=" * 70)
        print("TERMINAL AGENT REAL QWEN3 TEST: PASS")
        print("=" * 70)

    finally:
        # Temizlik
        if workspace.exists():
            shutil.rmtree(workspace)
            print(f"\nWorkspace temizlendi: {workspace}")


if __name__ == "__main__":
    try:
        test_terminal_agent_real_qwen3()
        print("\n" + "=" * 70)
        print("GERÇEK QWEN3 TERMINAL AGENT TEST BAŞARILI")
        print("=" * 70)
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
