"""
multiply.py için gerçek testler
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from quality_tests.tool_usage_workspace.multiply import multiply

# Testler
assert multiply(2, 3) == 6, f"multiply(2, 3) == 6 failed, got {multiply(2, 3)}"
print("multiply(2, 3) == 6: PASSED")

assert multiply(3, 4) == 12, f"multiply(3, 4) == 12 failed, got {multiply(3, 4)}"
print("multiply(3, 4) == 12: PASSED")

assert multiply(-2, 3) == -6, f"multiply(-2, 3) == -6 failed, got {multiply(-2, 3)}"
print("multiply(-2, 3) == -6: PASSED")

print("\nAll tests passed!")
