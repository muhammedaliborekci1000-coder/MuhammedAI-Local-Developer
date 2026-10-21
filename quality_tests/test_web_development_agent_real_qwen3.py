"""
Web Development Agent Real Qwen3 Test
Gerçek Qwen3 modeli ile web development agent entegrasyon testi.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.web_security import WebSecurity
from app.tools.web_project_detector import WebProjectDetector
from app.tools.http_inspector import HttpInspector
from app.tools.dev_server_manager import DevServerManager
from app.tools.web_preview import WebPreview
from app.core.config import PROJECT_ROOT


@pytest.mark.slow
def test_web_development_agent_real_qwen3():
    """
    TEST — Real Qwen3 Web Development Agent Integration
    
    Bu test gerçek Qwen3 modelini kullanarak web development agent'ın
    temel yeteneklerini doğrular:
    - Web project detection
    - Security validation
    - HTTP inspection
    - Dry-run
    """
    print("\n" + "=" * 70)
    print("REAL QWEN3 WEB DEVELOPMENT AGENT TEST")
    print("=" * 70)
    
    # 1. Web Security Test
    print("\n1. Web Security Test")
    print("-" * 70)
    security = WebSecurity()
    
    # Localhost allow
    assert security.is_localhost("localhost") is True
    assert security.is_localhost("127.0.0.1") is True
    print("Localhost allow: PASS")
    
    # External block
    valid, error = security.validate_url("http://example.com", allow_external=False)
    assert valid is False
    assert "External URL not allowed" in error
    print("External block: PASS")
    
    # Secret redaction
    redacted = security.redact_secrets("Authorization: Bearer abc123")
    assert "[REDACTED]" in redacted
    assert "abc123" not in redacted
    print("Secret redaction: PASS")
    
    # 2. Web Project Detector Test
    print("\n2. Web Project Detector Test")
    print("-" * 70)
    
    workspace = PROJECT_ROOT / "quality_tests" / "real_qwen3_web_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        # Create a simple Flask project
        (workspace / "app.py").write_text("""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'

if __name__ == '__main__':
    app.run()
""")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.is_web_project is True
        assert info.framework == "flask"
        assert info.likely_port == 5000
        print(f"Framework detected: {info.framework}")
        print(f"Likely port: {info.likely_port}")
        print("Web project detection: PASS")
        
        # 3. HTTP Inspector Test
        print("\n3. HTTP Inspector Test")
        print("-" * 70)
        
        inspector = HttpInspector()
        
        # HTML inspection
        html = "<html><head><title>Test</title></head><body>Hello</body></html>"
        html_analysis = inspector.inspect_html(html)
        
        assert html_analysis.title == "Test"
        print(f"HTML title: {html_analysis.title}")
        print("HTML inspection: PASS")
        
        # JSON inspection
        json_str = '{"status": "ok", "message": "test"}'
        json_analysis = inspector.inspect_json(json_str)
        
        assert json_analysis.valid is True
        assert json_analysis.root_type == "object"
        print(f"JSON root type: {json_analysis.root_type}")
        print("JSON inspection: PASS")
        
        # 4. Dev Server Manager Dry-Run Test
        print("\n4. Dev Server Manager Dry-Run Test")
        print("-" * 70)
        
        server_manager = DevServerManager(workspace)
        
        server_info = server_manager.start_server(
            command="python app.py",
            working_directory=str(workspace),
            expected_port=5000,
            dry_run=True
        )
        
        assert server_info.state.value == "STARTING"
        assert server_info.pid is None
        assert "[DRY-RUN" in server_info.stdout
        print(f"Server state: {server_info.state.value}")
        print(f"Dry-run stdout: {server_info.stdout[:50]}...")
        print("Dev server dry-run: PASS")
        
        # 5. Web Preview Dry-Run Test
        print("\n5. Web Preview Dry-Run Test")
        print("-" * 70)
        
        preview = WebPreview(workspace)
        
        result = preview.start_preview(dry_run=True)
        
        assert result.status == "stopped"
        assert result.port == 5000
        assert result.framework == "flask"
        print(f"Preview status: {result.status}")
        print(f"Preview URL: {result.url}")
        print(f"Framework: {result.framework}")
        print("Web preview dry-run: PASS")
        
        # 6. Cleanup
        print("\n6. Cleanup")
        print("-" * 70)
        
        preview.cleanup()
        server_manager.cleanup()
        
        print("Cleanup: PASS")
        
        print("\n" + "=" * 70)
        print("REAL QWEN3 WEB DEVELOPMENT AGENT TEST: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


if __name__ == "__main__":
    try:
        test_web_development_agent_real_qwen3()
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
