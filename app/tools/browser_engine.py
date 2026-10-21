"""
Browser Engine Detection
Sistemde mevcut browser automation altyapısını tespit et.
"""

from typing import Dict, Any, Optional
from enum import Enum


class EngineState(Enum):
    """Browser engine durumları."""
    AVAILABLE = "AVAILABLE"
    MISSING_PACKAGE = "MISSING_PACKAGE"
    MISSING_BROWSER = "MISSING_BROWSER"
    ERROR = "ERROR"
    READY = "READY"


class BrowserEngine:
    """
    Browser engine tespiti.
    
    Özellikler:
    - Playwright detection
    - Selenium detection
    - Browser binary detection
    - Engine state
    """
    
    def __init__(self):
        """BrowserEngine başlat."""
        self._check_engines()
    
    def _check_engines(self) -> None:
        """Mevcut engine'leri kontrol et."""
        self.playwright_available = self._check_playwright()
        self.selenium_available = self._check_selenium()
        
        # Engine seçimi
        if self.playwright_available:
            self.engine = "playwright"
            self.package_available = True
        elif self.selenium_available:
            self.engine = "selenium"
            self.package_available = True
        else:
            self.engine = "none"
            self.package_available = False
        
        # Browser kontrolü
        self.browser_available = self._check_browser()
        
        # State hesapla
        if not self.package_available:
            self.state = EngineState.MISSING_PACKAGE
        elif not self.browser_available:
            self.state = EngineState.MISSING_BROWSER
        else:
            self.state = EngineState.READY
    
    def _check_playwright(self) -> bool:
        """Playwright paketi kontrol et."""
        try:
            import importlib
            importlib.util.find_spec("playwright")
            return True
        except Exception:
            return False
    
    def _check_selenium(self) -> bool:
        """Selenium paketi kontrol et."""
        try:
            import importlib
            importlib.util.find_spec("selenium")
            return True
        except Exception:
            return False
    
    def _check_browser(self) -> bool:
        """Browser binary kontrol et."""
        # Windows'ta Chrome/Edge kontrolü
        import os
        import shutil
        
        # Common browser paths
        browser_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ]
        
        for path in browser_paths:
            if os.path.exists(path):
                return True
        
        # PATH'ta chrome/msedge var mı
        if shutil.which("chrome") or shutil.which("msedge"):
            return True
        
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Engine status döndür.
        
        Returns:
            Dict[str, Any]: Engine status
        """
        return {
            "engine": self.engine,
            "package_available": self.package_available,
            "browser_available": self.browser_available,
            "state": self.state.value,
            "ready": self.state == EngineState.READY,
        }
    
    def is_ready(self) -> bool:
        """
        Engine ready mi?
        
        Returns:
            bool: Ready mi
        """
        return self.state == EngineState.READY
    
    def get_installation_instructions(self) -> Optional[str]:
        """
        Kurulum talimatları döndür.
        
        Returns:
            Optional[str]: Kurulum talimatları
        """
        if self.state == EngineState.READY:
            return None
        
        if self.state == EngineState.MISSING_PACKAGE:
            return (
                "Browser automation package required. "
                "Install one of:\n"
                "  pip install playwright\n"
                "  playwright install chromium\n"
                "  OR\n"
                "  pip install selenium"
            )
        
        if self.state == EngineState.MISSING_BROWSER:
            return (
                "Browser binary not found. "
                "Install Chrome or Edge on Windows 11."
            )
        
        return "Unknown browser engine state"
