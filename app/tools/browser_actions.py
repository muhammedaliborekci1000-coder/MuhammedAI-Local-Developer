"""
Browser Actions
Element actions (click, type, fill, select, scroll vb.).
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum

from app.tools.browser_manager import BrowserManager
from app.tools.browser_inspector import PageElement


class ActionRisk(Enum):
    """Action risk seviyeleri."""
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"


@dataclass
class ActionResult:
    """Action sonucu."""
    success: bool
    action: str
    selector: str
    error: Optional[str]
    url_changed: bool
    new_url: Optional[str]
    element_exists: bool


class BrowserActions:
    """
    Browser actions.
    
    Özellikler:
    - click
    - type
    - fill
    - clear
    - select
    - check/uncheck
    - hover
    - focus
    - press
    - submit
    - scroll
    - Risk sınıflandırması
    - Secret protection
    """
    
    def __init__(self, browser_manager: BrowserManager):
        """
        Args:
            browser_manager: Browser manager
        """
        self.browser_manager = browser_manager
    
    def _get_risk(self, action: str) -> ActionRisk:
        """
        Action risk sınıflandırması.
        
        Args:
            action: Action adı
            
        Returns:
            ActionRisk: Risk seviyesi
        """
        safe_actions = {"inspect", "screenshot", "get_title", "get_url"}
        low_actions = {"scroll", "hover", "focus"}
        medium_actions = {"click", "type", "fill", "select", "submit"}
        high_actions = {"navigate", "file_upload", "download"}
        blocked_actions = {"javascript_inject", "cookie_extract", "secret_extract"}
        
        if action in safe_actions:
            return ActionRisk.SAFE
        elif action in low_actions:
            return ActionRisk.LOW
        elif action in medium_actions:
            return ActionRisk.MEDIUM
        elif action in high_actions:
            return ActionRisk.HIGH
        elif action in blocked_actions:
            return ActionRisk.BLOCKED
        else:
            return ActionRisk.MEDIUM
    
    def click(self, selector: str) -> ActionResult:
        """
        Elemente tıkla.
        
        Args:
            selector: CSS selector
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="click",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            old_url = self.browser_manager.current_url
            
            if self.browser_manager.engine.engine == "playwright":
                self._click_playwright(selector)
            elif self.browser_manager.engine.engine == "selenium":
                self._click_selenium(selector)
            
            new_url = self.browser_manager.current_url
            url_changed = old_url != new_url
            
            return ActionResult(
                success=True,
                action="click",
                selector=selector,
                error=None,
                url_changed=url_changed,
                new_url=new_url,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="click",
                selector=selector,
                error=f"Click failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _click_playwright(self, selector: str) -> None:
        """Playwright ile click."""
        self.browser_manager.page.click(selector)
    
    def _click_selenium(self, selector: str) -> None:
        """Selenium ile click."""
        from selenium.webdriver.common.by import By
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        element.click()
    
    def type(self, selector: str, text: str, sensitive: bool = False) -> ActionResult:
        """
        Elemente yaz.
        
        Args:
            selector: CSS selector
            text: Yazılacak metin
            sensitive: Sensitive mi (password vb.)
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="type",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        # Sensitive field kontrolü
        if sensitive and not self._is_sensitive_allowed():
            return ActionResult(
                success=False,
                action="type",
                selector=selector,
                error="Sensitive field requires explicit approval",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._type_playwright(selector, text)
            elif self.browser_manager.engine.engine == "selenium":
                self._type_selenium(selector, text)
            
            return ActionResult(
                success=True,
                action="type",
                selector=selector,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="type",
                selector=selector,
                error=f"Type failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _type_playwright(self, selector: str, text: str) -> None:
        """Playwright ile type."""
        self.browser_manager.page.fill(selector, text)
    
    def _type_selenium(self, selector: str, text: str) -> None:
        """Selenium ile type."""
        from selenium.webdriver.common.by import By
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        element.clear()
        element.send_keys(text)
    
    def fill(self, selector: str, value: str, sensitive: bool = False) -> ActionResult:
        """
        Elementi doldur.
        
        Args:
            selector: CSS selector
            value: Değer
            sensitive: Sensitive mi
            
        Returns:
            ActionResult: Action sonucu
        """
        return self.type(selector, value, sensitive)
    
    def clear(self, selector: str) -> ActionResult:
        """
        Elementi temizle.
        
        Args:
            selector: CSS selector
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="clear",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._clear_playwright(selector)
            elif self.browser_manager.engine.engine == "selenium":
                self._clear_selenium(selector)
            
            return ActionResult(
                success=True,
                action="clear",
                selector=selector,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="clear",
                selector=selector,
                error=f"Clear failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _clear_playwright(self, selector: str) -> None:
        """Playwright ile clear."""
        self.browser_manager.page.fill(selector, "")
    
    def _clear_selenium(self, selector: str) -> None:
        """Selenium ile clear."""
        from selenium.webdriver.common.by import By
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        element.clear()
    
    def select(self, selector: str, value: str) -> ActionResult:
        """
        Select option seç.
        
        Args:
            selector: CSS selector
            value: Değer
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="select",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._select_playwright(selector, value)
            elif self.browser_manager.engine.engine == "selenium":
                self._select_selenium(selector, value)
            
            return ActionResult(
                success=True,
                action="select",
                selector=selector,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="select",
                selector=selector,
                error=f"Select failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _select_playwright(self, selector: str, value: str) -> None:
        """Playwright ile select."""
        self.browser_manager.page.select_option(selector, value)
    
    def _select_selenium(self, selector: str, value: str) -> None:
        """Selenium ile select."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import Select
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        select = Select(element)
        select.select_by_value(value)
    
    def check(self, selector: str) -> ActionResult:
        """
        Checkbox işaretle.
        
        Args:
            selector: CSS selector
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="check",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._check_playwright(selector)
            elif self.browser_manager.engine.engine == "selenium":
                self._check_selenium(selector)
            
            return ActionResult(
                success=True,
                action="check",
                selector=selector,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="check",
                selector=selector,
                error=f"Check failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _check_playwright(self, selector: str) -> None:
        """Playwright ile check."""
        self.browser_manager.page.check(selector)
    
    def _check_selenium(self, selector: str) -> None:
        """Selenium ile check."""
        from selenium.webdriver.common.by import By
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        if not element.is_selected():
            element.click()
    
    def uncheck(self, selector: str) -> ActionResult:
        """
        Checkbox işaretini kaldır.
        
        Args:
            selector: CSS selector
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="uncheck",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._uncheck_playwright(selector)
            elif self.browser_manager.engine.engine == "selenium":
                self._uncheck_selenium(selector)
            
            return ActionResult(
                success=True,
                action="uncheck",
                selector=selector,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="uncheck",
                selector=selector,
                error=f"Uncheck failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _uncheck_playwright(self, selector: str) -> None:
        """Playwright ile uncheck."""
        self.browser_manager.page.uncheck(selector)
    
    def _uncheck_selenium(self, selector: str) -> None:
        """Selenium ile uncheck."""
        from selenium.webdriver.common.by import By
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        if element.is_selected():
            element.click()
    
    def hover(self, selector: str) -> ActionResult:
        """
        Element üzerinde hover.
        
        Args:
            selector: CSS selector
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="hover",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._hover_playwright(selector)
            elif self.browser_manager.engine.engine == "selenium":
                self._hover_selenium(selector)
            
            return ActionResult(
                success=True,
                action="hover",
                selector=selector,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="hover",
                selector=selector,
                error=f"Hover failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _hover_playwright(self, selector: str) -> None:
        """Playwright ile hover."""
        self.browser_manager.page.hover(selector)
    
    def _hover_selenium(self, selector: str) -> None:
        """Selenium ile hover."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.action_chains import ActionChains
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        ActionChains(self.browser_manager.browser).move_to_element(element).perform()
    
    def focus(self, selector: str) -> ActionResult:
        """
        Elemente focus.
        
        Args:
            selector: CSS selector
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="focus",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._focus_playwright(selector)
            elif self.browser_manager.engine.engine == "selenium":
                self._focus_selenium(selector)
            
            return ActionResult(
                success=True,
                action="focus",
                selector=selector,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="focus",
                selector=selector,
                error=f"Focus failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _focus_playwright(self, selector: str) -> None:
        """Playwright ile focus."""
        self.browser_manager.page.focus(selector)
    
    def _focus_selenium(self, selector: str) -> None:
        """Selenium ile focus."""
        from selenium.webdriver.common.by import By
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        self.browser_manager.browser.execute_script("arguments[0].focus();", element)
    
    def press(self, key: str) -> ActionResult:
        """
        Tuşa bas.
        
        Args:
            key: Tuş (Enter, Escape vb.)
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="press",
                selector=key,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._press_playwright(key)
            elif self.browser_manager.engine.engine == "selenium":
                self._press_selenium(key)
            
            return ActionResult(
                success=True,
                action="press",
                selector=key,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="press",
                selector=key,
                error=f"Press failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _press_playwright(self, key: str) -> None:
        """Playwright ile press."""
        self.browser_manager.page.keyboard.press(key)
    
    def _press_selenium(self, key: str) -> None:
        """Selenium ile press."""
        from selenium.webdriver.common.keys import Keys
        key_map = {
            "Enter": Keys.ENTER,
            "Escape": Keys.ESCAPE,
            "Tab": Keys.TAB,
            "Space": Keys.SPACE,
        }
        selenium_key = key_map.get(key, key)
        self.browser_manager.browser.find_element(By.TAG_NAME, "body").send_keys(selenium_key)
    
    def submit(self, selector: str) -> ActionResult:
        """
        Form submit.
        
        Args:
            selector: Form selector
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="submit",
                selector=selector,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            old_url = self.browser_manager.current_url
            
            if self.browser_manager.engine.engine == "playwright":
                self._submit_playwright(selector)
            elif self.browser_manager.engine.engine == "selenium":
                self._submit_selenium(selector)
            
            new_url = self.browser_manager.current_url
            url_changed = old_url != new_url
            
            return ActionResult(
                success=True,
                action="submit",
                selector=selector,
                error=None,
                url_changed=url_changed,
                new_url=new_url,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="submit",
                selector=selector,
                error=f"Submit failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _submit_playwright(self, selector: str) -> None:
        """Playwright ile submit."""
        self.browser_manager.page.evaluate(f"document.querySelector('{selector}').submit()")
    
    def _submit_selenium(self, selector: str) -> None:
        """Selenium ile submit."""
        from selenium.webdriver.common.by import By
        element = self.browser_manager.browser.find_element(By.CSS_SELECTOR, selector)
        element.submit()
    
    def scroll(self, direction: str = "down", amount: int = 500) -> ActionResult:
        """
        Scroll.
        
        Args:
            direction: up/down
            amount: Piksel miktarı
            
        Returns:
            ActionResult: Action sonucu
        """
        if self.browser_manager.state.value != "READY":
            return ActionResult(
                success=False,
                action="scroll",
                selector=direction,
                error="Browser not ready",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                self._scroll_playwright(direction, amount)
            elif self.browser_manager.engine.engine == "selenium":
                self._scroll_selenium(direction, amount)
            
            return ActionResult(
                success=True,
                action="scroll",
                selector=direction,
                error=None,
                url_changed=False,
                new_url=None,
                element_exists=True
            )
            
        except Exception as exc:
            return ActionResult(
                success=False,
                action="scroll",
                selector=direction,
                error=f"Scroll failed: {exc}",
                url_changed=False,
                new_url=None,
                element_exists=False
            )
    
    def _scroll_playwright(self, direction: str, amount: int) -> None:
        """Playwright ile scroll."""
        if direction == "down":
            self.browser_manager.page.evaluate(f"window.scrollBy(0, {amount})")
        else:
            self.browser_manager.page.evaluate(f"window.scrollBy(0, -{amount})")
    
    def _scroll_selenium(self, direction: str, amount: int) -> None:
        """Selenium ile scroll."""
        if direction == "down":
            self.browser_manager.browser.execute_script(f"window.scrollBy(0, {amount})")
        else:
            self.browser_manager.browser.execute_script(f"window.scrollBy(0, -{amount})")
    
    def _is_sensitive_allowed(self) -> bool:
        """
        Sensitive field izni var mı?
        
        Returns:
            bool: İzin var mı
        """
        # Şu an için false, approval mekanizması ile entegrasyon gerekebilir
        return False
