"""
MuhammedAI Local Developer - Project Rules
Proje kurallarını yöneten sistem.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

from app.core.config import PROJECT_ROOT


class RulePriority(Enum):
    """Rule öncelik seviyeleri."""
    SYSTEM_SECURITY = 1
    PROJECT_SECURITY = 2
    PROJECT_ARCHITECTURE = 3
    DIRECTORY = 4
    FILE_SPECIFIC = 5
    USER_TASK = 6


@dataclass
class Rule:
    """Kural kaydı."""
    content: str
    file_path: str
    priority: RulePriority = RulePriority.PROJECT_ARCHITECTURE
    tags: Set[str] = field(default_factory=set)


class ProjectRules:
    """
    Proje kurallarını yönetir.
    
    Özellikler:
    - Rules discovery
    - Rules parsing
    - Priority management
    - Relevance filtering
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
                        tags=tags
                    )
    
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
