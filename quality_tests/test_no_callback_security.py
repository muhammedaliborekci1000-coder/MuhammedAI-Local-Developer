"""
Quality Test: No Callback Security
Amaç: approval_callback=None olduğunda ChangeWorkflow'un güvenli olarak
reddettiğini doğrulamak.
"""

import pytest
from app.tools.change_workflow import ChangeWorkflow


class TestNoCallbackSecurity:
    """Callback yoksa güvenli davranış testleri."""

    def test_change_workflow_requires_approval(self):
        """
        ChangeWorkflow.apply_change approved=False olduğunda reddetmeli.
        """
        workflow = ChangeWorkflow()
        
        # Geçersiz plan
        plan = {
            "file": "test.py",
            "function": "hello",
            "problem": "change world to universe",
            "change": "modify return value",
            "old_code": "return 'world'",
            "new_code": "return 'universe'",
            "reason": "user request"
        }
        
        # approved=False ile çağır
        result = workflow.apply_change(plan, test_file="test.py", approved=False)
        
        # Reddedilmeli
        assert result["success"] is False
        assert result["status"] == "NOT_APPROVED"
        assert "onay" in result["message"].lower()

    def test_change_workflow_approved_allows(self):
        """
        ChangeWorkflow.apply_change approved=True olduğunda değişikliği denemeli.
        """
        workflow = ChangeWorkflow()
        
        # Geçerli plan (dosya gerçekten varsa)
        plan = {
            "file": "test.py",
            "function": "hello",
            "problem": "change world to universe",
            "change": "modify return value",
            "old_code": "return 'world'",
            "new_code": "return 'universe'",
            "reason": "user request"
        }
        
        # approved=True ile çağır
        result = workflow.apply_change(plan, test_file="test.py", approved=True)
        
        # Plan doğrulaması başarısız olabilir ama onay aşamasını geçmeli
        # approved=True ise NOT_APPROVED hatası olmamalı
        assert result["status"] != "NOT_APPROVED"
