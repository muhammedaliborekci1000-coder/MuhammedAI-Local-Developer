"""
MuhammedAI Local Developer - Project Rules
Proje kurallarını yöneten sistem.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime

from app.core.config import PROJECT_ROOT


class RulePriority(Enum):
    """Rule öncelik seviyeleri."""
    SYSTEM_SECURITY = 1
    PROJECT_SECURITY = 2
    PROJECT_ARCHITECTURE = 3
    DIRECTORY = 4
    FILE_SPECIFIC = 5
    USER_TASK = 6


class RuleSeverity(Enum):
    """Rule ciddiyet seviyeleri."""
    ERROR = "error"  # Kural ihlali hatayı engeller
    WARNING = "warning"  # Kural ihlali uyarı verir
    INFO = "info"  # Bilgilendirme
    SUGGESTION = "suggestion"  # Öneri


@dataclass
class Rule:
    """Kural kaydı."""
    content: str
    file_path: str
    priority: RulePriority = RulePriority.PROJECT_ARCHITECTURE
    tags: Set[str] = field(default_factory=set)
    severity: RuleSeverity = RuleSeverity.WARNING
    pattern: Optional[str] = None  # Regex pattern for validation
    enabled: bool = True  # Rule aktif/pasif
    created_at: datetime = field(default_factory=datetime.now)
    violation_count: int = 0  # İhlal sayısı


class ProjectRules:
    """
    Proje kurallarını yönetir.
    
    Özellikler:
    - Rules discovery
    - Rules parsing
    - Priority management
    - Relevance filtering
    - Rule validation
    - Conflict detection
    - Rule enforcement
    - Analytics
    """
    
    def __init__(self, project_root: Path = PROJECT_ROOT):
        """
        Args:
            project_root: Proje kök dizini
        """
        self.project_root = Path(project_root)
        self.rules_dir = self.project_root / ".muhammedai" / "rules"
        self.rules: Dict[str, Rule] = {}
        self._load_rules()
    
    def _load_rules(self) -> None:
        """Rules dosyalarını yükle."""
        if not self.rules_dir.exists():
            return
        
        for rule_file in self.rules_dir.glob("*.md"):
            try:
                self._parse_rule_file(rule_file)
            except Exception as e:
                print(f"Rule dosyası okuma hatası {rule_file}: {e}")
    
    def _parse_rule_file(self, rule_file: Path) -> None:
        """
        Rule dosyasını parse et.
        
        Args:
            rule_file: Rule dosyası yolu
        """
        # Dosya boyutu kontrolü
        if rule_file.stat().st_size > 100_000:  # 100KB limit
            print(f"Rule dosyası çok büyük: {rule_file}")
            return
        
        try:
            with open(rule_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Rule dosyası encoding hatası: {rule_file}")
            return
        
        # Path traversal kontrolü
        try:
            relative = rule_file.relative_to(self.rules_dir)
        except ValueError:
            print(f"Path traversal denemesi: {rule_file}")
            return
        
        # Priority belirle
        priority = self._determine_priority(rule_file.name)
        
        # Severity belirle
        severity = self._determine_severity(rule_file.name, content)
        
        # Pattern çıkar (varsa)
        pattern = self._extract_pattern(content)
        
        # Tags belirle
        tags = self._extract_tags(rule_file.name, content)
        
        # Satır bazlı rules
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            # Markdown bullet point
            if line.startswith('- '):
                rule_content = line[2:].strip()
                if rule_content:
                    rule_id = f"{relative}_{len(self.rules)}"
                    self.rules[rule_id] = Rule(
                        content=rule_content,
                        file_path=str(relative),
                        priority=priority,
                        severity=severity,
                        pattern=pattern,
                        tags=tags
                    )
    
    def _determine_severity(self, filename: str, content: str) -> RuleSeverity:
        """
        Dosya adı ve içeriğe göre severity belirle.
        
        Args:
            filename: Dosya adı
            content: İçerik
            
        Returns:
            RuleSeverity: Ciddiyet seviyesi
        """
        filename_lower = filename.lower()
        content_lower = content.lower()
        
        if "security" in filename_lower or "must" in content_lower or "never" in content_lower:
            return RuleSeverity.ERROR
        elif "should" in content_lower or "avoid" in content_lower:
            return RuleSeverity.WARNING
        elif "recommend" in content_lower or "suggest" in content_lower:
            return RuleSeverity.SUGGESTION
        else:
            return RuleSeverity.INFO
    
    def _extract_pattern(self, content: str) -> Optional[str]:
        """
        İçerikten regex pattern çıkar.
        
        Args:
            content: İçerik
            
        Returns:
            Optional[str]: Regex pattern veya None
        """
        # Pattern: /pattern/ formatında ara
        pattern_match = re.search(r'/([^/]+)/', content)
        if pattern_match:
            return pattern_match.group(1)
        return None
    
    def _determine_priority(self, filename: str) -> RulePriority:
        """
        Dosya adına göre priority belirle.
        
        Args:
            filename: Dosya adı
            
        Returns:
            RulePriority: Öncelik seviyesi
        """
        filename_lower = filename.lower()
        
        if "security" in filename_lower:
            return RulePriority.PROJECT_SECURITY
        elif "architecture" in filename_lower:
            return RulePriority.PROJECT_ARCHITECTURE
        else:
            return RulePriority.DIRECTORY
    
    def _extract_tags(self, filename: str, content: str) -> Set[str]:
        """
        Dosya adı ve içeriğinden tags çıkar.
        
        Args:
            filename: Dosya adı
            content: İçerik
            
        Returns:
            Set[str]: Tags
        """
        tags = set()
        filename_lower = filename.lower()
        
        # Dosya adından
        if "security" in filename_lower:
            tags.add("security")
        if "coding" in filename_lower:
            tags.add("coding")
        if "testing" in filename_lower:
            tags.add("testing")
        if "architecture" in filename_lower:
            tags.add("architecture")
        
        return tags
    
    def get_relevant_rules(
        self,
        task: Optional[str] = None,
        file_path: Optional[str] = None,
        tags: Optional[Set[str]] = None,
        max_rules: int = 20
    ) -> List[Rule]:
        """
        İlgili kuralları al.
        
        Args:
            task: Görev açıklaması (keyword matching için)
            file_path: Dosya yolu (directory matching için)
            tags: Tag filtresi
            max_rules: Maksimum kural sayısı
            
        Returns:
            List[Rule]: İlgili kurallar
        """
        results = []
        
        for rule in self.rules.values():
            # Tag filtresi
            if tags and not tags.intersection(rule.tags):
                continue
            
            # Task keyword matching
            if task:
                task_lower = task.lower()
                rule_lower = rule.content.lower()
                if any(keyword in rule_lower for keyword in task_lower.split()):
                    results.append(rule)
                    continue
            
            # Tüm rules (tag ile eşleşen)
            results.append(rule)
        
        # Priority sırala
        results.sort(key=lambda r: r.priority.value)
        
        return results[:max_rules]
    
    def get_all_rules(self) -> List[Rule]:
        """
        Tüm kuralları al.
        
        Returns:
            List[Rule]: Tüm kurallar
        """
        return list(self.rules.values())
    
    def reload(self) -> None:
        """Rules'ları yeniden yükle."""
        self.rules.clear()
        self._load_rules()
    
    def validate_rule(self, rule: Rule) -> Dict[str, Any]:
        """
        Rule validasyonu.
        
        Args:
            rule: Rule
            
        Returns:
            Dict: Validasyon sonucu
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Content boş mu?
        if not rule.content or not rule.content.strip():
            result["valid"] = False
            result["errors"].append("Rule content boş")
        
        # Pattern geçerli mi?
        if rule.pattern:
            try:
                re.compile(rule.pattern)
            except re.error as e:
                result["valid"] = False
                result["errors"].append(f"Geçersiz regex pattern: {e}")
        
        return result
    
    def detect_conflicts(self) -> List[Dict[str, Any]]:
        """
        Rule conflict detection.
        
        Returns:
            List[Dict]: Conflict listesi
        """
        conflicts = []
        rule_list = list(self.rules.values())
        
        for i, rule1 in enumerate(rule_list):
            for rule2 in rule_list[i+1:]:
                # Aynı tag'ler ve zıt severity
                if rule1.tags.intersection(rule2.tags):
                    if (rule1.severity == RuleSeverity.ERROR and 
                        rule2.severity == RuleSeverity.SUGGESTION):
                        conflicts.append({
                            "rule1": rule1.content,
                            "rule2": rule2.content,
                            "reason": "Zıt severity ile aynı tag'ler"
                        })
        
        return conflicts
    
    def enforce_rules(self, content: str, file_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Rule enforcement (content validation).
        
        Args:
            content: İçerik
            file_path: Dosya yolu
            
        Returns:
            List[Dict]: Violation listesi
        """
        violations = []
        
        for rule_id, rule in self.rules.items():
            if not rule.enabled:
                continue
            
            # Pattern matching
            if rule.pattern:
                try:
                    if re.search(rule.pattern, content):
                        violations.append({
                            "rule_id": rule_id,
                            "rule": rule.content,
                            "severity": rule.severity.value,
                            "file_path": file_path,
                            "message": f"Rule ihlali: {rule.content}"
                        })
                        rule.violation_count += 1
                except re.error:
                    pass
        
        return violations
    
    def get_analytics(self) -> Dict[str, Any]:
        """
        Rule analytics al.
        
        Returns:
            Dict: Analytics verileri
        """
        total_rules = len(self.rules)
        enabled_rules = sum(1 for r in self.rules.values() if r.enabled)
        disabled_rules = total_rules - enabled_rules
        
        severity_counts = {}
        priority_counts = {}
        tag_counts = {}
        total_violations = 0
        
        for rule in self.rules.values():
            # Severity counts
            sev = rule.severity.value
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            
            # Priority counts
            pri = rule.priority.name
            priority_counts[pri] = priority_counts.get(pri, 0) + 1
            
            # Tag counts
            for tag in rule.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            # Violations
            total_violations += rule.violation_count
        
        return {
            "total_rules": total_rules,
            "enabled_rules": enabled_rules,
            "disabled_rules": disabled_rules,
            "severity_counts": severity_counts,
            "priority_counts": priority_counts,
            "tag_counts": tag_counts,
            "total_violations": total_violations,
            "rules_dir": str(self.rules_dir)
        }
    
    def enable_rule(self, rule_id: str) -> bool:
        """
        Rule'ı aktif et.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            bool: Başarılı mı
        """
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
            return True
        return False
    
    def disable_rule(self, rule_id: str) -> bool:
        """
        Rule'ı pasif et.
        
        Args:
            rule_id: Rule ID
            
        Returns:
            bool: Başarılı mı
        """
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
            return True
        return False
