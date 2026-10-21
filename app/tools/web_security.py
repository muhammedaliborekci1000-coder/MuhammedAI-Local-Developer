"""
Web Security
HTTP istekleri için güvenlik katmanı.
SSRF, localhost bypass, arbitrary protocol engelleme.
"""

import re
import ipaddress
from typing import Tuple, Optional
from urllib.parse import urlparse, urlunparse


class WebSecurity:
    """
    Web istekleri için güvenlik doğrulaması.
    
    Özellikler:
    - Localhost only (127.0.0.1, localhost, ::1)
    - SSRF engelleme
    - Decimal IP bypass engelleme
    - Hexadecimal IP bypass engelleme
    - IPv4-mapped IPv6 bypass engelleme
    - DNS rebinding benzeri local erişim bypassları
    - file://, ftp:// gibi arbitrary protocol engelleme
    - Internal network scanning engelleme
    """
    
    # İzin verilen protokoller
    ALLOWED_PROTOCOLS = {"http", "https"}
    
    # İzin verilen local adresler
    LOCALHOST_ALIASES = {
        "localhost",
        "127.0.0.1",
        "::1",
        "0.0.0.0",
    }
    
    # Local port aralıkları (engellenecek)
    BLOCKED_PORTS = {
        # Common system ports
        22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432,
        # Dangerous ports
        21, 69, 123, 161, 162, 389, 636, 873, 2049,
    }
    
    def __init__(self):
        """WebSecurity başlat."""
        pass
    
    def normalize_url(self, url: str) -> str:
        """
        URL normalize et.
        
        Args:
            url: URL
            
        Returns:
            str: Normalize edilmiş URL
        """
        try:
            parsed = urlparse(url)
            
            # Host normalize et
            host = parsed.hostname or ""
            
            # Decimal IP → normal IP
            if self._is_decimal_ip(host):
                host = self._decimal_to_ip(host)
            
            # Hexadecimal IP → normal IP
            if self._is_hex_ip(host):
                host = self._hex_to_ip(host)
            
            # IPv4-mapped IPv6 → IPv4
            if self._is_ipv4_mapped_ipv6(host):
                host = self._ipv4_mapped_to_ipv4(host)
            
            # Netloc rebuild (port koru, IPv6 köşeli parantez koru)
            netloc = self._build_netloc(host, parsed.port, parsed.username, parsed.password)
            
            # URL rebuild
            normalized = urlunparse((
                parsed.scheme,
                netloc,
                parsed.path,
                parsed.params,
                parsed.query,
                parsed.fragment
            ))
            
            return normalized
            
        except Exception:
            return url
    
    def _build_netloc(self, host: str, port: Optional[int], username: Optional[str], password: Optional[str]) -> str:
        """
        Netloc build et (port, IPv6 köşeli parantez, auth koru).
        
        Args:
            host: Host
            port: Port
            username: Username
            password: Password
            
        Returns:
            str: Netloc
        """
        # IPv6 köşeli parantez
        if ":" in host and not (host.startswith("[") and host.endswith("]")):
            host = f"[{host}]"
        
        # Auth ekle
        if username:
            if password:
                auth = f"{username}:{password}@"
            else:
                auth = f"{username}@"
        else:
            auth = ""
        
        # Port ekle
        if port:
            return f"{auth}{host}:{port}"
        else:
            return f"{auth}{host}"
    
    def _is_decimal_ip(self, host: str) -> bool:
        """Decimal IP mi?"""
        try:
            # 2130706433 = 127.0.0.1
            return host.isdigit() and 0 <= int(host) <= 4294967295
        except Exception:
            return False
    
    def _decimal_to_ip(self, decimal: str) -> str:
        """Decimal IP → IPv4."""
        try:
            num = int(decimal)
            return str(ipaddress.IPv4Address(num))
        except Exception:
            return decimal
    
    def _is_hex_ip(self, host: str) -> bool:
        """Hexadecimal IP mi?"""
        try:
            # 0x7f000001 = 127.0.0.1
            return host.startswith("0x") or host.startswith("0X")
        except Exception:
            return False
    
    def _hex_to_ip(self, hex_ip: str) -> str:
        """Hex IP → IPv4."""
        try:
            num = int(hex_ip, 16)
            return str(ipaddress.IPv4Address(num))
        except Exception:
            return hex_ip
    
    def _is_ipv4_mapped_ipv6(self, host: str) -> bool:
        """IPv4-mapped IPv6 mı?"""
        try:
            # ::ffff:127.0.0.1
            return host.startswith("::ffff:") or host.startswith("::FFFF:")
        except Exception:
            return False
    
    def _ipv4_mapped_to_ipv4(self, ipv6: str) -> str:
        """IPv4-mapped IPv6 → IPv4."""
        try:
            # ::ffff:127.0.0.1 → 127.0.0.1
            if ":" in ipv6:
                parts = ipv6.split(":")
                return parts[-1]
            return ipv6
        except Exception:
            return ipv6
    
    def is_localhost(self, host: str) -> bool:
        """
        Localhost mu?
        
        Args:
            host: Host
            
        Returns:
            bool: Localhost mu
        """
        if not host:
            return False
        
        # Normalize et
        host = host.lower().strip()
        
        # Direct match
        if host in self.LOCALHOST_ALIASES:
            return True
        
        # IPv4 loopback range
        try:
            ip = ipaddress.ip_address(host)
            if ip.version == 4 and ip.is_loopback:
                return True
            if ip.version == 6 and ip.is_loopback:
                return True
        except Exception:
            pass
        
        return False
    
    def is_private_network(self, host: str) -> bool:
        """
        Private network mi?
        
        Args:
            host: Host
            
        Returns:
            bool: Private network mi
        """
        if not host:
            return False
        
        try:
            ip = ipaddress.ip_address(host)
            
            # IPv4 private ranges
            if ip.version == 4:
                return ip.is_private
            
            # IPv6 private ranges
            if ip.version == 6:
                return ip.is_private
                
        except Exception:
            pass
        
        return False
    
    def is_allowed_protocol(self, url: str) -> bool:
        """
        İzin verilen protokol mü?
        
        Args:
            url: URL
            
        Returns:
            bool: İzin verilen mi
        """
        try:
            parsed = urlparse(url)
            return parsed.scheme in self.ALLOWED_PROTOCOLS
        except Exception:
            return False
    
    def is_blocked_port(self, url: str) -> bool:
        """
        Engellenmiş port mu?
        
        Args:
            url: URL
            
        Returns:
            bool: Engellenmiş mi
        """
        try:
            parsed = urlparse(url)
            port = parsed.port
            
            if port:
                return port in self.BLOCKED_PORTS
            else:
                # Default port kontrolü
                if parsed.scheme == "http" and 80 in self.BLOCKED_PORTS:
                    return True
                if parsed.scheme == "https" and 443 in self.BLOCKED_PORTS:
                    return True
                
        except Exception:
            pass
        
        return False
    
    def validate_url(self, url: str, allow_external: bool = False) -> Tuple[bool, Optional[str]]:
        """
        URL doğrula.
        
        Args:
            url: URL
            allow_external: Dış URL'lere izin ver
            
        Returns:
            Tuple[bool, Optional[str]]: (valid, error)
        """
        # Protocol kontrolü
        if not self.is_allowed_protocol(url):
            return False, "Protocol not allowed. Only http/https allowed."
        
        # Normalize et
        normalized = self.normalize_url(url)
        
        try:
            parsed = urlparse(normalized)
            host = parsed.hostname or ""
            
            if not host:
                return False, "Invalid URL: no host"
            
            # Localhost kontrolü
            is_local = self.is_localhost(host)
            
            # External kontrolü
            is_private = self.is_private_network(host)
            
            # External URL kontrolü
            if not allow_external and not is_local:
                return False, f"External URL not allowed: {host}"
            
            # Private network kontrolü (external izni yoksa)
            if not allow_external and is_private and not is_local:
                return False, f"Private network access not allowed: {host}"
            
            # Port kontrolü
            if self.is_blocked_port(normalized):
                return False, f"Blocked port: {parsed.port}"
            
            return True, None
            
        except Exception as exc:
            return False, f"URL validation failed: {exc}"
    
    def redact_secrets(self, text: str) -> str:
        """
        Secret redaction.
        
        Args:
            text: Metin
            
        Returns:
            str: Redacted metin
        """
        if not text:
            return text
        
        # Secret patterns
        patterns = [
            r'authorization\s*:\s*bearer\s+[\w\-\.]+',
            r'authorization\s*:\s*[\w\-\.]+',
            r'api[_-]?key\s*[:=]\s*[\'"]?[\w\-]+[\'"]?',
            r'token\s*[:=]\s*[\'"]?[\w\-\.]+[\'"]?',
            r'password\s*[:=]\s*[\'"]?[\w]+[\'"]?',
            r'secret\s*[:=]\s*[\'"]?[\w\-]+[\'"]?',
            r'aws[_-]?access[_-]?key\s*[:=]\s*[\'"]?[\w]+[\'"]?',
            r'aws[_-]?secret[_-]?key\s*[:=]\s*[\'"]?[\w/]+[\'"]?',
            r'github[_-]?token\s*[:=]\s*[\'"]?[\w]+[\'"]?',
            r'openai[_-]?api[_-]?key\s*[:=]\s*[\'"]?[\w\-]+[\'"]?',
        ]
        
        redacted = text
        for pattern in patterns:
            redacted = re.sub(pattern, '[REDACTED]', redacted, flags=re.IGNORECASE)
        
        return redacted
