"""
Web Preview
Web development preview ve yönetim.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Any

from app.core.config import PROJECT_ROOT
from app.tools.web_project_detector import WebProjectDetector, WebProjectInfo
from app.tools.dev_server_manager import DevServerManager, ServerState, ServerInfo
from app.tools.http_inspector import HttpInspector, HttpResponse, HtmlAnalysis, JsonAnalysis
from app.tools.web_security import WebSecurity
from app.tools.browser_manager import BrowserManager
from app.tools.browser_inspector import BrowserInspector


@dataclass
class WebPreviewResult:
    """Web preview sonucu."""
    status: str  # running, stopped, failed
    url: str
    port: Optional[int]
    framework: str
    health: bool
    server_pid: Optional[int]
    http_response: Optional[HttpResponse]
    html_analysis: Optional[HtmlAnalysis]
    json_analysis: Optional[JsonAnalysis]
    error: Optional[str]


class WebPreview:
    """
    Web preview yöneticisi.
    
    Özellikler:
    - Web project detection
    - Dev server start/stop
    - Health check
    - HTTP inspection
    - HTML/JSON analysis
    - Browser preview URL generation
    """
    
    def __init__(self, project_root: Path = PROJECT_ROOT):
        """
        Args:
            project_root: Proje kök dizini
        """
        self.project_root = Path(project_root)
        
        self.detector = WebProjectDetector(project_root)
        self.server_manager = DevServerManager(project_root)
        self.http_inspector = HttpInspector()
        self.security = WebSecurity()
        self.browser_manager = BrowserManager()
        self.browser_inspector = BrowserInspector(self.browser_manager)
        
        self.active_preview: Optional[WebPreviewResult] = None
    
    def detect_project(self) -> WebProjectInfo:
        """
        Web projesi tespit et.
        
        Returns:
            WebProjectInfo: Web projesi bilgisi
        """
        return self.detector.detect(self.project_root)
    
    def start_preview(
        self,
        dry_run: bool = False
    ) -> WebPreviewResult:
        """
        Preview başlat.
        
        Args:
            dry_run: Dry-run
            
        Returns:
            WebPreviewResult: Preview sonucu
        """
        # Project detection
        project_info = self.detect_project()
        
        if not project_info.is_web_project:
            return WebPreviewResult(
                status="failed",
                url="",
                port=None,
                framework=project_info.framework,
                health=False,
                server_pid=None,
                http_response=None,
                html_analysis=None,
                json_analysis=None,
                error="Not a web project"
            )
        
        # Dry-run
        if dry_run:
            if project_info.is_web_project:
                return WebPreviewResult(
                    status="stopped",
                    url=f"http://127.0.0.1:{project_info.likely_port}",
                    port=project_info.likely_port,
                    framework=project_info.framework,
                    health=False,
                    server_pid=None,
                    http_response=None,
                    html_analysis=None,
                    json_analysis=None,
                    error=None
                )
            else:
                return WebPreviewResult(
                    status="failed",
                    url="",
                    port=None,
                    framework=project_info.framework,
                    health=False,
                    server_pid=None,
                    http_response=None,
                    html_analysis=None,
                    json_analysis=None,
                    error="Not a web project"
                )
        
        # Server start
        server_info = self.server_manager.start_server(
            command=project_info.start_command,
            working_directory=str(self.project_root),
            expected_port=project_info.likely_port,
            dry_run=False
        )
        
        if server_info.state != ServerState.RUNNING:
            return WebPreviewResult(
                status="failed",
                url="",
                port=server_info.port,
                framework=project_info.framework,
                health=False,
                server_pid=server_info.pid,
                http_response=None,
                html_analysis=None,
                json_analysis=None,
                error=server_info.error or "Server failed to start"
            )
        
        # URL oluştur
        url = f"http://127.0.0.1:{server_info.port}"
        
        # HTTP inspection
        http_response = self.http_inspector.get(url, timeout=10)
        
        # HTML/JSON analysis
        html_analysis = None
        json_analysis = None
        
        if http_response.success and http_response.content_type:
            if "text/html" in http_response.content_type:
                html_analysis = self.http_inspector.inspect_html(http_response.body)
            elif "application/json" in http_response.content_type:
                json_analysis = self.http_inspector.inspect_json(http_response.body)
        
        # Preview result
        result = WebPreviewResult(
            status="running",
            url=url,
            port=server_info.port,
            framework=project_info.framework,
            health=server_info.health_check_passed,
            server_pid=server_info.pid,
            http_response=http_response,
            html_analysis=html_analysis,
            json_analysis=json_analysis,
            error=None
        )
        
        self.active_preview = result
        return result
    
    def stop_preview(self) -> bool:
        """
        Preview durdur.
        
        Returns:
            bool: Başarılı mı
        """
        if self.active_preview and self.active_preview.server_pid:
            success = self.server_manager.stop_server(self.active_preview.server_pid)
            if success:
                self.active_preview = None
            return success
        return False
    
    def health_check(self) -> Dict[str, Any]:
        """
        Health check.
        
        Returns:
            Dict[str, Any]: Health check sonucu
        """
        if not self.active_preview or not self.active_preview.url:
            return {
                "healthy": False,
                "error": "No active preview"
            }
        
        return self.http_inspector.health_check(self.active_preview.url)
    
    def get_preview_url(self) -> Optional[str]:
        """
        Preview URL al.
        
        Returns:
            Optional[str]: Preview URL
        """
        if self.active_preview:
            return self.active_preview.url
        return None
    
    def cleanup(self) -> None:
        """Temizlik."""
        self.stop_preview()
        self.server_manager.cleanup()
        self.browser_manager.cleanup()
    
    def launch_browser(self, headless: bool = True) -> Dict[str, Any]:
        """
        Browser başlat.
        
        Args:
            headless: Headless mode
            
        Returns:
            Dict[str, Any]: Browser launch sonucu
        """
        info = self.browser_manager.launch(headless)
        
        return {
            "state": info.state.value,
            "error": info.error,
        }
    
    def navigate_browser(self, url: str, allow_external: bool = False) -> Dict[str, Any]:
        """
        Browser ile URL'e git.
        
        Args:
            url: URL
            allow_external: Dış URL'lere izin ver
            
        Returns:
            Dict[str, Any]: Navigation sonucu
        """
        info = self.browser_manager.navigate(url, allow_external)
        
        return {
            "state": info.state.value,
            "url": info.url,
            "title": info.title,
            "error": info.error,
        }
    
    def inspect_browser_page(self) -> Dict[str, Any]:
        """
        Browser sayfasını incele.
        
        Returns:
            Dict[str, Any]: Page inspection sonucu
        """
        page_info = self.browser_inspector.inspect_page()
        
        return {
            "url": page_info.url,
            "title": page_info.title,
            "headings_count": len(page_info.headings),
            "links_count": len(page_info.links),
            "buttons_count": len(page_info.buttons),
            "inputs_count": len(page_info.inputs),
            "forms_count": len(page_info.forms),
            "error": page_info.error,
        }
    
    def close_browser(self) -> bool:
        """
        Browser kapat.
        
        Returns:
            bool: Başarılı mı
        """
        return self.browser_manager.close()
