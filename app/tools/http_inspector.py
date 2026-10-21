"""
HTTP Inspector
HTTP istekleri ve response analizi.
"""

import json
import re
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from urllib.parse import urlparse

from app.tools.web_security import WebSecurity


@dataclass
class HttpResponse:
    """HTTP response."""
    status_code: int
    headers: Dict[str, str]
    content_type: str
    content_length: int
    body: str
    response_time: float
    final_url: str
    success: bool
    error: Optional[str]


@dataclass
class HtmlAnalysis:
    """HTML analizi."""
    title: str
    scripts: List[str]
    stylesheets: List[str]
    links: List[str]
    forms: List[str]
    images: List[str]
    missing_resources: List[str]
    parse_errors: List[str]


@dataclass
class JsonAnalysis:
    """JSON analizi."""
    valid: bool
    root_type: str
    keys: List[str]
    parse_error: Optional[str]


class HttpInspector:
    """
    HTTP istekleri ve response analizi.
    
    Özellikler:
    - GET, HEAD istekleri
    - status_code, headers, content_type, content_length, body
    - response_time, final_url
    - Body limit
    - Secret redaction
    - HTML inspection
    - JSON inspection
    """
    
    def __init__(self, max_body_size: int = 100000):
        """
        Args:
            max_body_size: Maksimum body boyutu (bytes)
        """
        self.max_body_size = max_body_size
        self.security = WebSecurity()
    
    def get(
        self,
        url: str,
        timeout: int = 10,
        allow_external: bool = False
    ) -> HttpResponse:
        """
        GET isteği.
        
        Args:
            url: URL
            timeout: Timeout (saniye)
            allow_external: Dış URL'lere izin ver
            
        Returns:
            HttpResponse: HTTP response
        """
        return self._request("GET", url, timeout, allow_external)
    
    def head(
        self,
        url: str,
        timeout: int = 10,
        allow_external: bool = False
    ) -> HttpResponse:
        """
        HEAD isteği.
        
        Args:
            url: URL
            timeout: Timeout (saniye)
            allow_external: Dış URL'lere izin ver
            
        Returns:
            HttpResponse: HTTP response
        """
        return self._request("HEAD", url, timeout, allow_external)
    
    def _request(
        self,
        method: str,
        url: str,
        timeout: int,
        allow_external: bool
    ) -> HttpResponse:
        """
        HTTP isteği.
        
        Args:
            method: HTTP method
            url: URL
            timeout: Timeout
            allow_external: Dış URL'lere izin ver
            
        Returns:
            HttpResponse: HTTP response
        """
        start_time = time.time()
        
        # URL doğrula
        valid, error = self.security.validate_url(url, allow_external)
        if not valid:
            return HttpResponse(
                status_code=0,
                headers={},
                content_type="",
                content_length=0,
                body="",
                response_time=time.time() - start_time,
                final_url=url,
                success=False,
                error=error
            )
        
        try:
            import urllib.request
            import urllib.error
            
            # Request oluştur
            req = urllib.request.Request(url, method=method)
            
            # İsteği gönder
            with urllib.request.urlopen(req, timeout=timeout) as response:
                status_code = response.status
                headers = dict(response.headers)
                content_type = headers.get("Content-Type", "")
                
                # Body oku (GET için)
                body = ""
                if method == "GET":
                    raw_body = response.read(self.max_body_size)
                    body = raw_body.decode("utf-8", errors="ignore")
                
                # Secret redaction
                body = self.security.redact_secrets(body)
                
                return HttpResponse(
                    status_code=status_code,
                    headers=headers,
                    content_type=content_type,
                    content_length=len(body),
                    body=body,
                    response_time=time.time() - start_time,
                    final_url=response.url,
                    success=True,
                    error=None
                )
                
        except urllib.error.HTTPError as e:
            return HttpResponse(
                status_code=e.code,
                headers=dict(e.headers) if e.headers else {},
                content_type="",
                content_length=0,
                body="",
                response_time=time.time() - start_time,
                final_url=url,
                success=False,
                error=f"HTTP Error: {e.code}"
            )
            
        except urllib.error.URLError as e:
            return HttpResponse(
                status_code=0,
                headers={},
                content_type="",
                content_length=0,
                body="",
                response_time=time.time() - start_time,
                final_url=url,
                success=False,
                error=f"URL Error: {e.reason}"
            )
            
        except Exception as e:
            return HttpResponse(
                status_code=0,
                headers={},
                content_type="",
                content_length=0,
                body="",
                response_time=time.time() - start_time,
                final_url=url,
                success=False,
                error=f"Request failed: {e}"
            )
    
    def inspect_html(self, body: str) -> HtmlAnalysis:
        """
        HTML analizi.
        
        Args:
            body: HTML body
            
        Returns:
            HtmlAnalysis: HTML analizi
        """
        title = ""
        scripts = []
        stylesheets = []
        links = []
        forms = []
        images = []
        missing_resources = []
        parse_errors = []
        
        try:
            # Title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', body, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
            
            # Scripts
            script_matches = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', body, re.IGNORECASE)
            scripts = script_matches
            
            # Stylesheets
            link_matches = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', body, re.IGNORECASE)
            stylesheets = link_matches
            
            # Links
            a_matches = re.findall(r'<a[^>]*href=["\']([^"\']+)["\']', body, re.IGNORECASE)
            links = a_matches
            
            # Forms
            form_matches = re.findall(r'<form[^>]*action=["\']([^"\']*)["\']', body, re.IGNORECASE)
            forms = form_matches
            
            # Images
            img_matches = re.findall(r'<img[^>]*src=["\']([^"\']+)["\']', body, re.IGNORECASE)
            images = img_matches
            
        except Exception as e:
            parse_errors.append(f"HTML parse error: {e}")
        
        return HtmlAnalysis(
            title=title,
            scripts=scripts,
            stylesheets=stylesheets,
            links=links,
            forms=forms,
            images=images,
            missing_resources=missing_resources,
            parse_errors=parse_errors
        )
    
    def inspect_json(self, body: str) -> JsonAnalysis:
        """
        JSON analizi.
        
        Args:
            body: JSON body
            
        Returns:
            JsonAnalysis: JSON analizi
        """
        try:
            data = json.loads(body)
            
            # Root type
            if isinstance(data, dict):
                root_type = "object"
                keys = list(data.keys())
            elif isinstance(data, list):
                root_type = "array"
                keys = []
            else:
                root_type = type(data).__name__
                keys = []
            
            return JsonAnalysis(
                valid=True,
                root_type=root_type,
                keys=keys,
                parse_error=None
            )
            
        except json.JSONDecodeError as e:
            return JsonAnalysis(
                valid=False,
                root_type="",
                keys=[],
                parse_error=f"JSON parse error: {e}"
            )
        except Exception as e:
            return JsonAnalysis(
                valid=False,
                root_type="",
                keys=[],
                parse_error=f"JSON analysis error: {e}"
            )
    
    def health_check(
        self,
        url: str,
        timeout: int = 10,
        allow_external: bool = False
    ) -> Dict[str, Any]:
        """
        Health check.
        
        Args:
            url: URL
            timeout: Timeout
            allow_external: Dış URL'lere izin ver
            
        Returns:
            Dict[str, Any]: Health check sonucu
        """
        response = self.get(url, timeout, allow_external)
        
        return {
            "healthy": response.success and response.status_code == 200,
            "status_code": response.status_code,
            "response_time_ms": response.response_time * 1000,
            "content_type": response.content_type,
            "errors": [response.error] if response.error else []
        }
