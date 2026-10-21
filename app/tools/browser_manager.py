"""
Browser Manager
Browser başlatma, yönetme ve kontrol etme.
"""

import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from app.tools.browser_engine import BrowserEngine, EngineState
from app.tools.web_security import WebSecurity


class BrowserState(Enum):
    """Browser durumları."""
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    NAVIGATING = "NAVIGATING"
    READY = "READY"
    ERROR = "ERROR"
    CLOSING = "CLOSING"
    CLOSED = "CLOSED"


@dataclass
class BrowserInfo:
    """Browser bilgisi."""
    state: BrowserState
    url: Optional[str]
    title: Optional[str]
    viewport: Dict[str, int]
    console_errors: List[str]
    page_errors: List[str]
    network_errors: List[Dict[str, Any]]
    screenshot_path: Optional[str]
    error: Optional[str]


class BrowserManager:
    """
    Browser yöneticisi.
    
    Özellikler:
    - Browser launch/close
    - Context/page creation
    - Navigation
    - Reload
    - Screenshot
    - Console log collection
    - Page error collection
    - Network error collection
    """
    
    def __init__(self):
        """BrowserManager başlat."""
        self.engine = BrowserEngine()
        self.security = WebSecurity()
        
        self.browser = None
        self.context = None
        self.page = None
        self.session_id = None
        
        self.state = BrowserState.CLOSED
        self.current_url = None
        self.current_title = None
        self.console_errors = []
        self.page_errors = []
        self.network_errors = []
    
    def is_ready(self) -> bool:
        """
        Browser ready mi?
        
        Returns:
            bool: Ready mi
        """
        return self.engine.is_ready()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Browser status döndür.
        
        Returns:
            Dict[str, Any]: Browser status
        """
        return {
            "engine_status": self.engine.get_status(),
            "browser_state": self.state.value,
            "current_url": self.current_url,
            "current_title": self.current_title,
            "console_errors_count": len(self.console_errors),
            "page_errors_count": len(self.page_errors),
            "network_errors_count": len(self.network_errors),
        }
    
    def launch(self, headless: bool = True) -> BrowserInfo:
        """
        Browser başlat.
        
        Args:
            headless: Headless mode
            
        Returns:
            BrowserInfo: Browser bilgisi
        """
        if not self.engine.is_ready():
            return BrowserInfo(
                state=BrowserState.ERROR,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error=self.engine.get_installation_instructions()
            )
        
        try:
            self.state = BrowserState.STARTING
            
            # Playwright kullan
            if self.engine.engine == "playwright":
                return self._launch_playwright(headless)
            # Selenium kullan
            elif self.engine.engine == "selenium":
                return self._launch_selenium(headless)
            else:
                return BrowserInfo(
                    state=BrowserState.ERROR,
                    url=None,
                    title=None,
                    viewport={},
                    console_errors=[],
                    page_errors=[],
                    network_errors=[],
                    screenshot_path=None,
                    error="No browser engine available"
                )
                
        except Exception as exc:
            self.state = BrowserState.ERROR
            return BrowserInfo(
                state=BrowserState.ERROR,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error=f"Failed to launch browser: {exc}"
            )
    
    def _launch_playwright(self, headless: bool) -> BrowserInfo:
        """Playwright ile browser başlat."""
        from playwright.sync_api import sync_playwright
        
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        
        # Console error listener
        self.page.on("console", self._on_console)
        self.page.on("pageerror", self._on_page_error)
        self.page.on("requestfailed", self._on_request_failed)
        
        self.session_id = f"playwright-{int(time.time())}"
        self.state = BrowserState.READY
        
        return BrowserInfo(
            state=BrowserState.READY,
            url=None,
            title=None,
            viewport={"width": 1280, "height": 720},
            console_errors=[],
            page_errors=[],
            network_errors=[],
            screenshot_path=None,
            error=None
        )
    
    def _launch_selenium(self, headless: bool) -> BrowserInfo:
        """Selenium ile browser başlat."""
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        if headless:
            options.add_argument("--headless")
        
        self.browser = webdriver.Chrome(options=options)
        self.session_id = f"selenium-{int(time.time())}"
        self.state = BrowserState.READY
        
        return BrowserInfo(
            state=BrowserState.READY,
            url=None,
            title=None,
            viewport={"width": 1280, "height": 720},
            console_errors=[],
            page_errors=[],
            network_errors=[],
            screenshot_path=None,
            error=None
        )
    
    def _on_console(self, msg) -> None:
        """Console mesajı yakala."""
        if msg.type == "error":
            self.console_errors.append(msg.text)
    
    def _on_page_error(self, error) -> None:
        """Page error yakala."""
        self.page_errors.append(str(error))
    
    def _on_request_failed(self, request) -> None:
        """Request failure yakala."""
        self.network_errors.append({
            "url": request.url,
            "method": request.method,
            "failure": request.failure
        })
    
    def navigate(self, url: str, allow_external: bool = False) -> BrowserInfo:
        """
        URL'e git.
        
        Args:
            url: URL
            allow_external: Dış URL'lere izin ver
            
        Returns:
            BrowserInfo: Browser bilgisi
        """
        if self.state != BrowserState.READY:
            return BrowserInfo(
                state=self.state,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error="Browser not ready"
            )
        
        # URL doğrula
        valid, error = self.security.validate_url(url, allow_external)
        if not valid:
            return BrowserInfo(
                state=BrowserState.ERROR,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error=error
            )
        
        try:
            self.state = BrowserState.NAVIGATING
            start_time = time.time()
            
            if self.engine.engine == "playwright":
                self.page.goto(url, wait_until="networkidle")
                self.current_url = self.page.url
                self.current_title = self.page.title()
            elif self.engine.engine == "selenium":
                self.browser.get(url)
                self.current_url = self.browser.current_url
                self.current_title = self.browser.title
            
            response_time = time.time() - start_time
            self.state = BrowserState.READY
            
            return BrowserInfo(
                state=BrowserState.READY,
                url=self.current_url,
                title=self.current_title,
                viewport={"width": 1280, "height": 720},
                console_errors=self.console_errors.copy(),
                page_errors=self.page_errors.copy(),
                network_errors=self.network_errors.copy(),
                screenshot_path=None,
                error=None
            )
            
        except Exception as exc:
            self.state = BrowserState.ERROR
            return BrowserInfo(
                state=BrowserState.ERROR,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error=f"Navigation failed: {exc}"
            )
    
    def reload(self) -> BrowserInfo:
        """
        Sayfayı yenile.
        
        Returns:
            BrowserInfo: Browser bilgisi
        """
        if self.state != BrowserState.READY or not self.current_url:
            return BrowserInfo(
                state=self.state,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error="Cannot reload: no page loaded"
            )
        
        try:
            if self.engine.engine == "playwright":
                self.page.reload(wait_until="networkidle")
                self.current_url = self.page.url
                self.current_title = self.page.title()
            elif self.engine.engine == "selenium":
                self.browser.refresh()
                self.current_url = self.browser.current_url
                self.current_title = self.browser.title
            
            return BrowserInfo(
                state=BrowserState.READY,
                url=self.current_url,
                title=self.current_title,
                viewport={"width": 1280, "height": 720},
                console_errors=self.console_errors.copy(),
                page_errors=self.page_errors.copy(),
                network_errors=self.network_errors.copy(),
                screenshot_path=None,
                error=None
            )
            
        except Exception as exc:
            self.state = BrowserState.ERROR
            return BrowserInfo(
                state=BrowserState.ERROR,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error=f"Reload failed: {exc}"
            )
    
    def screenshot(self, path: Optional[str] = None) -> BrowserInfo:
        """
        Screenshot al.
        
        Args:
            path: Screenshot yolu
            
        Returns:
            BrowserInfo: Browser bilgisi
        """
        if self.state != BrowserState.READY:
            return BrowserInfo(
                state=self.state,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error="Browser not ready"
            )
        
        try:
            if path is None:
                path = f"screenshot_{int(time.time())}.png"
            
            if self.engine.engine == "playwright":
                self.page.screenshot(path=path)
            elif self.engine.engine == "selenium":
                self.browser.save_screenshot(path)
            
            return BrowserInfo(
                state=BrowserState.READY,
                url=self.current_url,
                title=self.current_title,
                viewport={"width": 1280, "height": 720},
                console_errors=self.console_errors.copy(),
                page_errors=self.page_errors.copy(),
                network_errors=self.network_errors.copy(),
                screenshot_path=path,
                error=None
            )
            
        except Exception as exc:
            return BrowserInfo(
                state=BrowserState.ERROR,
                url=None,
                title=None,
                viewport={},
                console_errors=[],
                page_errors=[],
                network_errors=[],
                screenshot_path=None,
                error=f"Screenshot failed: {exc}"
            )
    
    def close(self) -> bool:
        """
        Browser kapat.
        
        Returns:
            bool: Başarılı mı
        """
        try:
            self.state = BrowserState.CLOSING
            
            if self.engine.engine == "playwright":
                if self.page:
                    self.page.close()
                if self.context:
                    self.context.close()
                if self.browser:
                    self.browser.close()
                if self.playwright:
                    self.playwright.stop()
            elif self.engine.engine == "selenium":
                if self.browser:
                    self.browser.quit()
            
            self.state = BrowserState.CLOSED
            self.browser = None
            self.context = None
            self.page = None
            self.session_id = None
            self.current_url = None
            self.current_title = None
            self.console_errors = []
            self.page_errors = []
            self.network_errors = []
            
            return True
            
        except Exception:
            # Even if there's an error, ensure state is CLOSED
            self.state = BrowserState.CLOSED
            self.browser = None
            self.context = None
            self.page = None
            self.session_id = None
            self.current_url = None
            self.current_title = None
            self.console_errors = []
            self.page_errors = []
            self.network_errors = []
            return False
    
    def cleanup(self) -> None:
        """Temizlik."""
        if self.state != BrowserState.CLOSED:
            self.close()
