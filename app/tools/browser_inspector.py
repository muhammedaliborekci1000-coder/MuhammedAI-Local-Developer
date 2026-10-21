"""
Browser Inspector
DOM ve sayfa bilgisi toplama.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from app.tools.browser_manager import BrowserManager
from app.tools.web_security import WebSecurity


@dataclass
class PageElement:
    """Sayfa elementi."""
    tag: str
    text: str
    id: Optional[str]
    classes: List[str]
    role: Optional[str]
    name: Optional[str]
    type: Optional[str]
    visible: bool
    selector: str


@dataclass
class PageInfo:
    """Sayfa bilgisi."""
    url: str
    title: str
    visible_text: str
    headings: List[PageElement]
    links: List[PageElement]
    buttons: List[PageElement]
    inputs: List[PageElement]
    textareas: List[PageElement]
    selects: List[PageElement]
    forms: List[PageElement]
    images: List[PageElement]
    error: Optional[str]


class BrowserInspector:
    """
    Browser inspector.
    
    Özellikler:
    - DOM extraction
    - Title
    - Visible text
    - Headings
    - Links
    - Buttons
    - Inputs
    - Textareas
    - Selects
    - Forms
    - Images
    - Secret redaction
    """
    
    def __init__(self, browser_manager: BrowserManager):
        """
        Args:
            browser_manager: Browser manager
        """
        self.browser_manager = browser_manager
        self.security = WebSecurity()
    
    def inspect_page(self) -> PageInfo:
        """
        Sayfayı incele.
        
        Returns:
            PageInfo: Sayfa bilgisi
        """
        if self.browser_manager.state.value != "READY":
            return PageInfo(
                url="",
                title="",
                visible_text="",
                headings=[],
                links=[],
                buttons=[],
                inputs=[],
                textareas=[],
                selects=[],
                forms=[],
                images=[],
                error="Browser not ready"
            )
        
        try:
            if self.browser_manager.engine.engine == "playwright":
                return self._inspect_playwright()
            elif self.browser_manager.engine.engine == "selenium":
                return self._inspect_selenium()
            else:
                return PageInfo(
                    url="",
                    title="",
                    visible_text="",
                    headings=[],
                    links=[],
                    buttons=[],
                    inputs=[],
                    textareas=[],
                    selects=[],
                    forms=[],
                    images=[],
                    error="No browser engine"
                )
                
        except Exception as exc:
            return PageInfo(
                url="",
                title="",
                visible_text="",
                headings=[],
                links=[],
                buttons=[],
                inputs=[],
                textareas=[],
                selects=[],
                forms=[],
                images=[],
                error=f"Inspection failed: {exc}"
            )
    
    def _inspect_playwright(self) -> PageInfo:
        """Playwright ile sayfa incele."""
        page = self.browser_manager.page
        
        # Title
        title = page.title()
        
        # URL
        url = page.url
        
        # Visible text
        visible_text = page.inner_text("body") if page.query_selector("body") else ""
        
        # Headings
        headings = self._get_headings_playwright(page)
        
        # Links
        links = self._get_links_playwright(page)
        
        # Buttons
        buttons = self._get_buttons_playwright(page)
        
        # Inputs
        inputs = self._get_inputs_playwright(page)
        
        # Textareas
        textareas = self._get_textareas_playwright(page)
        
        # Selects
        selects = self._get_selects_playwright(page)
        
        # Forms
        forms = self._get_forms_playwright(page)
        
        # Images
        images = self._get_images_playwright(page)
        
        return PageInfo(
            url=url,
            title=title,
            visible_text=visible_text[:1000],  # Limit
            headings=headings,
            links=links,
            buttons=buttons,
            inputs=inputs,
            textareas=textareas,
            selects=selects,
            forms=forms,
            images=images,
            error=None
        )
    
    def _inspect_selenium(self) -> PageInfo:
        """Selenium ile sayfa incele."""
        from selenium.webdriver.common.by import By
        
        browser = self.browser_manager.browser
        
        # Title
        title = browser.title
        
        # URL
        url = browser.current_url
        
        # Visible text
        try:
            visible_text = browser.find_element(By.TAG_NAME, "body").text
        except:
            visible_text = ""
        
        # Headings
        headings = self._get_headings_selenium(browser)
        
        # Links
        links = self._get_links_selenium(browser)
        
        # Buttons
        buttons = self._get_buttons_selenium(browser)
        
        # Inputs
        inputs = self._get_inputs_selenium(browser)
        
        # Textareas
        textareas = self._get_textareas_selenium(browser)
        
        # Selects
        selects = self._get_selects_selenium(browser)
        
        # Forms
        forms = self._get_forms_selenium(browser)
        
        # Images
        images = self._get_images_selenium(browser)
        
        return PageInfo(
            url=url,
            title=title,
            visible_text=visible_text[:1000],  # Limit
            headings=headings,
            links=links,
            buttons=buttons,
            inputs=inputs,
            textareas=textareas,
            selects=selects,
            forms=forms,
            images=images,
            error=None
        )
    
    def _get_headings_playwright(self, page) -> List[PageElement]:
        """Headings al (Playwright)."""
        headings = []
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            elements = page.query_selector_all(tag)
            for el in elements:
                text = el.inner_text()
                elem_id = el.get_attribute("id")
                classes = el.get_attribute("class") or ""
                class_list = classes.split() if classes else []
                
                headings.append(PageElement(
                    tag=tag,
                    text=text[:100],
                    id=elem_id,
                    classes=class_list,
                    role=None,
                    name=None,
                    type=None,
                    visible=el.is_visible(),
                    selector=tag
                ))
        return headings
    
    def _get_links_playwright(self, page) -> List[PageElement]:
        """Links al (Playwright)."""
        links = []
        elements = page.query_selector_all("a")
        for el in elements:
            text = el.inner_text()
            href = el.get_attribute("href")
            elem_id = el.get_attribute("id")
            classes = el.get_attribute("class") or ""
            class_list = classes.split() if classes else []
            
            links.append(PageElement(
                tag="a",
                text=text[:100],
                id=elem_id,
                classes=class_list,
                role=None,
                name=None,
                type=None,
                visible=el.is_visible(),
                selector="a"
            ))
        return links
    
    def _get_buttons_playwright(self, page) -> List[PageElement]:
        """Buttons al (Playwright)."""
        buttons = []
        elements = page.query_selector_all("button")
        for el in elements:
            text = el.inner_text()
            elem_id = el.get_attribute("id")
            classes = el.get_attribute("class") or ""
            class_list = classes.split() if classes else []
            role = el.get_attribute("role")
            
            buttons.append(PageElement(
                tag="button",
                text=text[:100],
                id=elem_id,
                classes=class_list,
                role=role,
                name=None,
                type=None,
                visible=el.is_visible(),
                selector="button"
            ))
        return buttons
    
    def _get_inputs_playwright(self, page) -> List[PageElement]:
        """Inputs al (Playwright)."""
        inputs = []
        elements = page.query_selector_all("input")
        for el in elements:
            elem_id = el.get_attribute("id")
            classes = el.get_attribute("class") or ""
            class_list = classes.split() if classes else []
            name = el.get_attribute("name")
            input_type = el.get_attribute("type")
            
            # Password field redaction
            if input_type == "password":
                name = "[REDACTED]"
            
            inputs.append(PageElement(
                tag="input",
                text="",
                id=elem_id,
                classes=class_list,
                role=None,
                name=name,
                type=input_type,
                visible=el.is_visible(),
                selector="input"
            ))
        return inputs
    
    def _get_textareas_playwright(self, page) -> List[PageElement]:
        """Textareas al (Playwright)."""
        textareas = []
        elements = page.query_selector_all("textarea")
        for el in elements:
            elem_id = el.get_attribute("id")
            classes = el.get_attribute("class") or ""
            class_list = classes.split() if classes else []
            name = el.get_attribute("name")
            
            textareas.append(PageElement(
                tag="textarea",
                text="",
                id=elem_id,
                classes=class_list,
                role=None,
                name=name,
                type=None,
                visible=el.is_visible(),
                selector="textarea"
            ))
        return textareas
    
    def _get_selects_playwright(self, page) -> List[PageElement]:
        """Selects al (Playwright)."""
        selects = []
        elements = page.query_selector_all("select")
        for el in elements:
            elem_id = el.get_attribute("id")
            classes = el.get_attribute("class") or ""
            class_list = classes.split() if classes else []
            name = el.get_attribute("name")
            
            selects.append(PageElement(
                tag="select",
                text="",
                id=elem_id,
                classes=class_list,
                role=None,
                name=name,
                type=None,
                visible=el.is_visible(),
                selector="select"
            ))
        return selects
    
    def _get_forms_playwright(self, page) -> List[PageElement]:
        """Forms al (Playwright)."""
        forms = []
        elements = page.query_selector_all("form")
        for el in elements:
            elem_id = el.get_attribute("id")
            classes = el.get_attribute("class") or ""
            class_list = classes.split() if classes else []
            action = el.get_attribute("action")
            
            forms.append(PageElement(
                tag="form",
                text=action or "",
                id=elem_id,
                classes=class_list,
                role=None,
                name=None,
                type=None,
                visible=el.is_visible(),
                selector="form"
            ))
        return forms
    
    def _get_images_playwright(self, page) -> List[PageElement]:
        """Images al (Playwright)."""
        images = []
        elements = page.query_selector_all("img")
        for el in elements:
            src = el.get_attribute("src")
            elem_id = el.get_attribute("id")
            classes = el.get_attribute("class") or ""
            class_list = classes.split() if classes else []
            
            images.append(PageElement(
                tag="img",
                text=src or "",
                id=elem_id,
                classes=class_list,
                role=None,
                name=None,
                type=None,
                visible=el.is_visible(),
                selector="img"
            ))
        return images
    
    # Selenium helper methods
    def _get_headings_selenium(self, browser) -> List[PageElement]:
        """Headings al (Selenium)."""
        from selenium.webdriver.common.by import By
        headings = []
        for tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            elements = browser.find_elements(By.TAG_NAME, tag)
            for el in elements:
                headings.append(PageElement(
                    tag=tag,
                    text=el.text[:100],
                    id=el.get_attribute("id"),
                    classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                    role=None,
                    name=None,
                    type=None,
                    visible=el.is_displayed(),
                    selector=tag
                ))
        return headings
    
    def _get_links_selenium(self, browser) -> List[PageElement]:
        """Links al (Selenium)."""
        from selenium.webdriver.common.by import By
        links = []
        elements = browser.find_elements(By.TAG_NAME, "a")
        for el in elements:
            links.append(PageElement(
                tag="a",
                text=el.text[:100],
                id=el.get_attribute("id"),
                classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                role=None,
                name=None,
                type=None,
                visible=el.is_displayed(),
                selector="a"
            ))
        return links
    
    def _get_buttons_selenium(self, browser) -> List[PageElement]:
        """Buttons al (Selenium)."""
        from selenium.webdriver.common.by import By
        buttons = []
        elements = browser.find_elements(By.TAG_NAME, "button")
        for el in elements:
            buttons.append(PageElement(
                tag="button",
                text=el.text[:100],
                id=el.get_attribute("id"),
                classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                role=el.get_attribute("role"),
                name=None,
                type=None,
                visible=el.is_displayed(),
                selector="button"
            ))
        return buttons
    
    def _get_inputs_selenium(self, browser) -> List[PageElement]:
        """Inputs al (Selenium)."""
        from selenium.webdriver.common.by import By
        inputs = []
        elements = browser.find_elements(By.TAG_NAME, "input")
        for el in elements:
            input_type = el.get_attribute("type")
            name = el.get_attribute("name")
            
            if input_type == "password":
                name = "[REDACTED]"
            
            inputs.append(PageElement(
                tag="input",
                text="",
                id=el.get_attribute("id"),
                classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                role=None,
                name=name,
                type=input_type,
                visible=el.is_displayed(),
                selector="input"
            ))
        return inputs
    
    def _get_textareas_selenium(self, browser) -> List[PageElement]:
        """Textareas al (Selenium)."""
        from selenium.webdriver.common.by import By
        textareas = []
        elements = browser.find_elements(By.TAG_NAME, "textarea")
        for el in elements:
            textareas.append(PageElement(
                tag="textarea",
                text="",
                id=el.get_attribute("id"),
                classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                role=None,
                name=el.get_attribute("name"),
                type=None,
                visible=el.is_displayed(),
                selector="textarea"
            ))
        return textareas
    
    def _get_selects_selenium(self, browser) -> List[PageElement]:
        """Selects al (Selenium)."""
        from selenium.webdriver.common.by import By
        selects = []
        elements = browser.find_elements(By.TAG_NAME, "select")
        for el in elements:
            selects.append(PageElement(
                tag="select",
                text="",
                id=el.get_attribute("id"),
                classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                role=None,
                name=el.get_attribute("name"),
                type=None,
                visible=el.is_displayed(),
                selector="select"
            ))
        return selects
    
    def _get_forms_selenium(self, browser) -> List[PageElement]:
        """Forms al (Selenium)."""
        from selenium.webdriver.common.by import By
        forms = []
        elements = browser.find_elements(By.TAG_NAME, "form")
        for el in elements:
            forms.append(PageElement(
                tag="form",
                text=el.get_attribute("action") or "",
                id=el.get_attribute("id"),
                classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                role=None,
                name=None,
                type=None,
                visible=el.is_displayed(),
                selector="form"
            ))
        return forms
    
    def _get_images_selenium(self, browser) -> List[PageElement]:
        """Images al (Selenium)."""
        from selenium.webdriver.common.by import By
        images = []
        elements = browser.find_elements(By.TAG_NAME, "img")
        for el in elements:
            images.append(PageElement(
                tag="img",
                text=el.get_attribute("src") or "",
                id=el.get_attribute("id"),
                classes=el.get_attribute("class").split() if el.get_attribute("class") else [],
                role=None,
                name=None,
                type=None,
                visible=el.is_displayed(),
                selector="img"
            ))
        return images
