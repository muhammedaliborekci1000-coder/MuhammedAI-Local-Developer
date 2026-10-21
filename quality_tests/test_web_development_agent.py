"""
Web Development Agent Tests
Web development özellikleri için testler.
"""

import pytest
import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tools.web_security import WebSecurity
from app.tools.web_project_detector import WebProjectDetector, WebProjectInfo
from app.tools.http_inspector import HttpInspector, HttpResponse, HtmlAnalysis, JsonAnalysis
from app.tools.dev_server_manager import DevServerManager, ServerState
from app.tools.web_preview import WebPreview, WebPreviewResult
from app.core.config import PROJECT_ROOT


def test_web_security_localhost_allow():
    """TEST 1 — Localhost allow."""
    print("\n" + "=" * 70)
    print("TEST 1 — Localhost Allow")
    print("=" * 70)

    security = WebSecurity()
    
    assert security.is_localhost("localhost") is True
    assert security.is_localhost("127.0.0.1") is True
    assert security.is_localhost("::1") is True
    
    print("Localhost allow: PASS")
    print("=" * 70)


def test_web_security_external_block():
    """TEST 2 — External URL block."""
    print("\n" + "=" * 70)
    print("TEST 2 — External URL Block")
    print("=" * 70)

    security = WebSecurity()
    
    valid, error = security.validate_url("http://example.com", allow_external=False)
    assert valid is False
    assert "External URL not allowed" in error
    
    print("External URL block: PASS")
    print("=" * 70)


def test_web_security_protocol_block():
    """TEST 3 — Protocol block."""
    print("\n" + "=" * 70)
    print("TEST 3 — Protocol Block")
    print("=" * 70)

    security = WebSecurity()
    
    valid, error = security.validate_url("file:///etc/passwd")
    assert valid is False
    assert "Protocol not allowed" in error
    
    print("Protocol block: PASS")
    print("=" * 70)


def test_web_security_secret_redaction():
    """TEST 4 — Secret redaction."""
    print("\n" + "=" * 70)
    print("TEST 4 — Secret Redaction")
    print("=" * 70)

    security = WebSecurity()
    
    redacted = security.redact_secrets("Authorization: Bearer abc123")
    assert "[REDACTED]" in redacted
    assert "abc123" not in redacted
    
    print("Secret redaction: PASS")
    print("=" * 70)


def test_web_security_decimal_ip():
    """TEST 5 — Decimal IP normalization."""
    print("\n" + "=" * 70)
    print("TEST 5 — Decimal IP Normalization")
    print("=" * 70)

    security = WebSecurity()
    
    normalized = security.normalize_url("http://2130706433")
    assert "127.0.0.1" in normalized
    
    print("Decimal IP normalization: PASS")
    print("=" * 70)


def test_flask_detection():
    """TEST 6 — Flask detection."""
    print("\n" + "=" * 70)
    print("TEST 6 — Flask Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "flask_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
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
        
        print("Flask detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_fastapi_detection():
    """TEST 7 — FastAPI detection."""
    print("\n" + "=" * 70)
    print("TEST 7 — FastAPI Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "fastapi_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "main.py").write_text("""
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def read_root():
    return {'Hello': 'World'}
""")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.is_web_project is True
        assert info.framework == "fastapi"
        assert info.likely_port == 8000
        
        print("FastAPI detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_django_detection():
    """TEST 8 — Django detection."""
    print("\n" + "=" * 70)
    print("TEST 8 — Django Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "django_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "manage.py").write_text("# Django manage.py")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.is_web_project is True
        assert info.framework == "django"
        assert info.likely_port == 8000
        
        print("Django detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_vite_detection():
    """TEST 9 — Vite detection."""
    print("\n" + "=" * 70)
    print("TEST 9 — Vite Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "vite_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "package.json").write_text('{"name": "test", "devDependencies": {"vite": "^5.0"}}')
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.is_web_project is True
        assert info.framework == "vite"
        assert info.likely_port == 5173
        
        print("Vite detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_next_detection():
    """TEST 10 — Next.js detection."""
    print("\n" + "=" * 70)
    print("TEST 10 — Next.js Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "next_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "package.json").write_text('{"name": "test", "dependencies": {"next": "^14.0"}}')
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.is_web_project is True
        assert info.framework == "next"
        assert info.likely_port == 3000
        
        print("Next.js detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_static_html_detection():
    """TEST 11 — Static HTML detection."""
    print("\n" + "=" * 70)
    print("TEST 11 — Static HTML Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "static_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "index.html").write_text("<html><body>Hello</body></html>")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.is_web_project is True
        assert info.framework == "static-html"
        
        print("Static HTML detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_unknown_project():
    """TEST 12 — Unknown project."""
    print("\n" + "=" * 70)
    print("TEST 12 — Unknown Project")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "unknown_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "readme.txt").write_text("Not a web project")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.is_web_project is False
        assert info.framework == "unknown"
        
        print("Unknown project: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_http_inspector_get():
    """TEST 13 — HTTP GET."""
    print("\n" + "=" * 70)
    print("TEST 13 — HTTP GET")
    print("=" * 70)

    inspector = HttpInspector()
    
    # Localhost test (fail expected since no server running)
    response = inspector.get("http://127.0.0.1:9999", timeout=1)
    
    assert response is not None
    assert response.success is False  # No server running
    
    print("HTTP GET: PASS")
    print("=" * 70)


def test_http_inspector_head():
    """TEST 14 — HTTP HEAD."""
    print("\n" + "=" * 70)
    print("TEST 14 — HTTP HEAD")
    print("=" * 70)

    inspector = HttpInspector()
    
    response = inspector.head("http://127.0.0.1:9999", timeout=1)
    
    assert response is not None
    assert response.success is False  # No server running
    
    print("HTTP HEAD: PASS")
    print("=" * 70)


def test_html_inspection():
    """TEST 15 — HTML inspection."""
    print("\n" + "=" * 70)
    print("TEST 15 — HTML Inspection")
    print("=" * 70)

    inspector = HttpInspector()
    
    html = """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <script src="app.js"></script>
        <link rel="stylesheet" href="style.css">
        <img src="logo.png">
    </body>
    </html>
    """
    
    analysis = inspector.inspect_html(html)
    
    assert analysis.title == "Test Page"
    assert "app.js" in analysis.scripts
    assert "style.css" in analysis.stylesheets
    assert "logo.png" in analysis.images
    
    print("HTML inspection: PASS")
    print("=" * 70)


def test_json_inspection():
    """TEST 16 — JSON inspection."""
    print("\n" + "=" * 70)
    print("TEST 16 — JSON Inspection")
    print("=" * 70)

    inspector = HttpInspector()
    
    json_str = '{"name": "test", "value": 123}'
    
    analysis = inspector.inspect_json(json_str)
    
    assert analysis.valid is True
    assert analysis.root_type == "object"
    assert "name" in analysis.keys
    assert "value" in analysis.keys
    
    print("JSON inspection: PASS")
    print("=" * 70)


def test_json_inspection_invalid():
    """TEST 17 — Invalid JSON inspection."""
    print("\n" + "=" * 70)
    print("TEST 17 — Invalid JSON Inspection")
    print("=" * 70)

    inspector = HttpInspector()
    
    analysis = inspector.inspect_json("not valid json")
    
    assert analysis.valid is False
    assert analysis.parse_error is not None
    
    print(" JSON inspection: PASS")
    print("=" * 70)


def test_dev_server_manager_dry_run():
    """TEST 18 — Dev server dry-run."""
    print("\n" + "=" * 70)
    print("TEST 18 — Dev Server Dry-Run")
    print("=" * 70)

    manager = DevServerManager()
    
    server_info = manager.start_server(
        command="python -m http.server",
        dry_run=True
    )
    
    assert server_info.state == ServerState.STARTING
    assert server_info.pid is None
    assert "[DRY-RUN" in server_info.stdout
    
    print("Dev server dry-run: PASS")
    print("=" * 70)


def test_dev_server_manager_port_check():
    """TEST 19 — Port check."""
    print("\n" + "=" * 70)
    print("TEST 19 — Port Check")
    print("=" * 70)

    manager = DevServerManager()
    
    # Random port check
    in_use = manager.check_port(99999)
    
    # Should return False for unused port
    assert isinstance(in_use, bool)
    
    print("Port check: PASS")
    print("=" * 70)


def test_web_preview_dry_run():
    """TEST 20 — Web preview dry-run."""
    print("\n" + "=" * 70)
    print("TEST 20 — Web Preview Dry-Run")
    print("=" * 70)

    preview = WebPreview()
    
    result = preview.start_preview(dry_run=True)
    
    # Current project is not a web project, so it should fail
    assert result.status == "failed"
    assert result.health is False
    assert result.server_pid is None
    
    print("Web preview dry-run: PASS")
    print("=" * 70)


def test_web_preview_detect_project():
    """TEST 21 — Web preview detect project."""
    print("\n" + "=" * 70)
    print("TEST 21 — Web Preview Detect Project")
    print("=" * 70)

    preview = WebPreview()
    
    info = preview.detect_project()
    
    # Current project is not a web project
    assert info is not None
    
    print("Web preview detect project: PASS")
    print("=" * 70)


def test_web_preview_cleanup():
    """TEST 22 — Web preview cleanup."""
    print("\n" + "=" * 70)
    print("TEST 22 — Web Preview Cleanup")
    print("=" * 70)

    preview = WebPreview()
    
    # Should not raise error
    preview.cleanup()
    
    print("Web preview cleanup: PASS")
    print("=" * 70)


def test_web_security_ipv4_mapped():
    """TEST 23 — IPv4-mapped IPv6."""
    print("\n" + "=" * 70)
    print("TEST 23 — IPv4-Mapped IPv6")
    print("=" * 70)

    security = WebSecurity()
    
    # Test the helper function directly
    ipv4 = security._ipv4_mapped_to_ipv4("::ffff:127.0.0.1")
    assert "127.0.0.1" in ipv4
    
    print("IPv4-mapped IPv6: PASS")
    print("=" * 70)


def test_web_security_hex_ip():
    """TEST 24 — Hex IP normalization."""
    print("\n" + "=" * 70)
    print("TEST 24 — Hex IP Normalization")
    print("=" * 70)

    security = WebSecurity()
    
    normalized = security.normalize_url("http://0x7f000001")
    assert "127.0.0.1" in normalized
    
    print("Hex IP normalization: PASS")
    print("=" * 70)


def test_web_security_private_network():
    """TEST 25 — Private network detection."""
    print("\n" + "=" * 70)
    print("TEST 25 — Private Network Detection")
    print("=" * 70)

    security = WebSecurity()
    
    assert security.is_private_network("192.168.1.1") is True
    assert security.is_private_network("10.0.0.1") is True
    assert security.is_private_network("8.8.8.8") is False
    
    print("Private network detection: PASS")
    print("=" * 70)


def test_web_security_blocked_port():
    """TEST 26 — Blocked port."""
    print("\n" + "=" * 70)
    print("TEST 26 — Blocked Port")
    print("=" * 70)

    security = WebSecurity()
    
    valid, error = security.validate_url("http://127.0.0.1:22")
    assert valid is False
    assert "Blocked port" in error
    
    print("Blocked port: PASS")
    print("=" * 70)


def test_http_inspector_body_limit():
    """TEST 27 — Body limit."""
    print("\n" + "=" * 70)
    print("TEST 27 — Body Limit")
    print("=" * 70)

    inspector = HttpInspector(max_body_size=100)
    
    assert inspector.max_body_size == 100
    
    print("Body limit: PASS")
    print("=" * 70)


def test_web_project_detector_package_manager():
    """TEST 28 — Package manager detection."""
    print("\n" + "=" * 70)
    print("TEST 28 — Package Manager Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "npm_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "package.json").write_text('{"name": "test", "dependencies": {"vite": "^5.0"}}')
        (workspace / "package-lock.json").write_text("{}")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.package_manager == "npm"
        
        print("Package manager detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_web_project_detector_pnpm():
    """TEST 29 — pnpm detection."""
    print("\n" + "=" * 70)
    print("TEST 29 — pnpm Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "pnpm_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "package.json").write_text('{"name": "test", "dependencies": {"vite": "^5.0"}}')
        (workspace / "pnpm-lock.yaml").write_text("")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.package_manager == "pnpm"
        
        print("pnpm detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_web_project_detector_yarn():
    """TEST 30 — Yarn detection."""
    print("\n" + "=" * 70)
    print("TEST 30 — Yarn Detection")
    print("=" * 70)

    workspace = PROJECT_ROOT / "quality_tests" / "yarn_workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    
    try:
        (workspace / "package.json").write_text('{"name": "test", "dependencies": {"vite": "^5.0"}}')
        (workspace / "yarn.lock").write_text("")
        
        detector = WebProjectDetector(workspace)
        info = detector.detect()
        
        assert info.package_manager == "yarn"
        
        print("Yarn detection: PASS")
        print("=" * 70)
        
    finally:
        if workspace.exists():
            shutil.rmtree(workspace)


def test_web_security_localhost_variations():
    """TEST 31 — Localhost variations."""
    print("\n" + "=" * 70)
    print("TEST 31 — Localhost Variations")
    print("=" * 70)

    security = WebSecurity()
    
    assert security.is_localhost("localhost") is True
    assert security.is_localhost("LOCALHOST") is True
    assert security.is_localhost("LocalHost") is True
    
    print("Localhost variations: PASS")
    print("=" * 70)


def test_web_security_secret_patterns():
    """TEST 32 — Secret patterns."""
    print("\n" + "=" * 70)
    print("TEST 32 — Secret Patterns")
    print("=" * 70)

    security = WebSecurity()
    
    text = "api_key=secret123 token=abc password=def"
    redacted = security.redact_secrets(text)
    
    assert "[REDACTED]" in redacted
    assert "secret123" not in redacted
    assert "abc" not in redacted
    assert "def" not in redacted
    
    print("Secret patterns: PASS")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_web_security_localhost_allow()
        test_web_security_external_block()
        test_web_security_protocol_block()
        test_web_security_secret_redaction()
        test_web_security_decimal_ip()
        test_flask_detection()
        test_fastapi_detection()
        test_django_detection()
        test_vite_detection()
        test_next_detection()
        test_static_html_detection()
        test_unknown_project()
        test_http_inspector_get()
        test_http_inspector_head()
        test_html_inspection()
        test_json_inspection()
        test_json_inspection_invalid()
        test_dev_server_manager_dry_run()
        test_dev_server_manager_port_check()
        test_web_preview_dry_run()
        test_web_preview_detect_project()
        test_web_preview_cleanup()
        test_web_security_ipv4_mapped()
        test_web_security_hex_ip()
        test_web_security_private_network()
        test_web_security_blocked_port()
        test_http_inspector_body_limit()
        test_web_project_detector_package_manager()
        test_web_project_detector_pnpm()
        test_web_project_detector_yarn()
        test_web_security_localhost_variations()
        test_web_security_secret_patterns()

        print("\n" + "=" * 70)
        print("WEB DEVELOPMENT AGENT TESTLERİ BAŞARILI")
        print("=" * 70)
        sys.exit(0)
    except Exception as e:
        print(f"\nTEST HATASI:")
        print("-" * 70)
        import traceback
        traceback.print_exc()
        print("=" * 70)
        sys.exit(1)
