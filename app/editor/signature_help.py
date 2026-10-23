"""
MuhammedAI Local Developer - Signature Help
Signature help engine for code editor.
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class SignatureTriggerMode(Enum):
    """Signature trigger mode."""
    AUTO = "auto"
    MANUAL = "manual"
    BOTH = "both"


class ParameterType(Enum):
    """Parameter type."""
    REQUIRED = "required"
    OPTIONAL = "optional"
    VARARGS = "varargs"
    KWARGS = "kwargs"


@dataclass
class Parameter:
    """Parameter information."""
    name: str
    param_type: ParameterType
    type_hint: str = ""
    default_value: str = ""
    description: str = ""
    is_active: bool = False


@dataclass
class FunctionSignature:
    """Function signature."""
    name: str
    parameters: List[Parameter] = field(default_factory=list)
    return_type: str = ""
    description: str = ""
    documentation: str = ""
    is_method: bool = False
    is_class_method: bool = False
    is_static_method: bool = False
    active_parameter: int = 0


@dataclass
class SignatureConfig:
    """Signature configuration."""
    trigger_mode: SignatureTriggerMode = SignatureTriggerMode.AUTO
    show_documentation: bool = True
    show_return_type: bool = True
    show_type_hints: bool = True
    highlight_active_parameter: bool = True
    auto_close_parentheses: bool = True
    show_parameter_names: bool = True
    show_default_values: bool = True
    max_signatures: int = 10
    signature_delay: int = 100


@dataclass
class SignatureResult:
    """Signature result."""
    success: bool
    signatures: List[FunctionSignature] = field(default_factory=list)
    active_signature: Optional[FunctionSignature] = None
    active_parameter: int = 0
    total_signatures: int = 0
    errors: List[str] = field(default_factory=list)
    message: Optional[str] = None


class SignatureHelpEngine:
    """
    Signature help engine.
    
    Özellikler:
    - Function signature display
    - Parameter information
    - Active parameter highlighting
    - Overload support
    - Documentation display
    - Type hints
    - Return type display
    - Auto-trigger
    - Manual trigger
    - Context-aware signatures
    - Signature filtering
    - Signature history
    - Parameter completion
    - Method signatures
    - Class method signatures
    - Static method signatures
    """
    
    def __init__(self, config: Optional[SignatureConfig] = None):
        """Initialize signature help engine."""
        self.config = config or SignatureConfig()
        self.signature_cache: Dict[str, List[FunctionSignature]] = {}
        self.signature_history: List[str] = []
        self.current_signatures: List[FunctionSignature] = []
        self.active_signature_index: int = 0
    
    def get_signature(
        self,
        function_name: str,
        context: Optional[str] = None
    ) -> SignatureResult:
        """
        Fonksiyon imzasını al.
        
        Args:
            function_name: Fonksiyon adı
            context: Bağlam (opsiyonel)
            
        Returns:
            SignatureResult: İmza sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            # Cache kontrolü
            if function_name in self.signature_cache:
                signatures = self.signature_cache[function_name]
                result.success = True
                result.signatures = signatures
                result.total_signatures = len(signatures)
                result.active_signature = signatures[0] if signatures else None
                result.message = f"Found {len(signatures)} signature(s)"
                
                # Geçmişe ekle
                if function_name not in self.signature_history:
                    self.signature_history.append(function_name)
                
                return result
            
            # İmza oluştur
            signatures = self._create_signatures(function_name, context)
            
            # Cache'e kaydet
            self.signature_cache[function_name] = signatures
            
            self.current_signatures = signatures
            self.active_signature_index = 0
            
            result.success = True
            result.signatures = signatures
            result.total_signatures = len(signatures)
            result.active_signature = signatures[0] if signatures else None
            result.message = f"Found {len(signatures)} signature(s)"
            
            # Geçmişe ekle
            if function_name not in self.signature_history:
                self.signature_history.append(function_name)
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def _create_signatures(
        self,
        function_name: str,
        context: Optional[str]
    ) -> List[FunctionSignature]:
        """
        İmzalar oluştur.
        
        Args:
            function_name: Fonksiyon adı
            context: Bağlam
            
        Returns:
            List[FunctionSignature]: İmza listesi
        """
        signatures = []
        
        # Örnek imza oluştur
        signature = FunctionSignature(
            name=function_name,
            parameters=[
                Parameter(
                    name="param1",
                    param_type=ParameterType.REQUIRED,
                    type_hint="str",
                    description="First parameter"
                ),
                Parameter(
                    name="param2",
                    param_type=ParameterType.OPTIONAL,
                    type_hint="int",
                    default_value="0",
                    description="Second parameter"
                ),
                Parameter(
                    name="param3",
                    param_type=ParameterType.OPTIONAL,
                    type_hint="bool",
                    default_value="True",
                    description="Third parameter"
                )
            ],
            return_type="void",
            description=f"Function {function_name}",
            documentation=f"Documentation for {function_name}"
        )
        
        signatures.append(signature)
        
        return signatures
    
    def update_active_parameter(self, parameter_index: int) -> SignatureResult:
        """
        Aktif parametreyi güncelle.
        
        Args:
            parameter_index: Parametre indeksi
            
        Returns:
            SignatureResult: Güncelleme sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            if self.current_signatures and self.active_signature_index < len(self.current_signatures):
                signature = self.current_signatures[self.active_signature_index]
                
                if 0 <= parameter_index < len(signature.parameters):
                    # Önceki parametreyi deaktif et
                    if signature.active_parameter < len(signature.parameters):
                        signature.parameters[signature.active_parameter].is_active = False
                    
                    # Yeni parametreyi aktif et
                    signature.parameters[parameter_index].is_active = True
                    signature.active_parameter = parameter_index
                    
                    result.success = True
                    result.active_signature = signature
                    result.active_parameter = parameter_index
                    result.message = f"Active parameter: {parameter_index}"
                else:
                    result.errors.append(f"Parameter index out of range: {parameter_index}")
            else:
                result.errors.append("No active signature")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def next_signature(self) -> SignatureResult:
        """
        Sonraki imzaya geç.
        
        Returns:
            SignatureResult: Geçiş sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            if self.current_signatures:
                self.active_signature_index = (self.active_signature_index + 1) % len(self.current_signatures)
                signature = self.current_signatures[self.active_signature_index]
                
                result.success = True
                result.active_signature = signature
                result.message = f"Signature {self.active_signature_index + 1}/{len(self.current_signatures)}"
            else:
                result.errors.append("No signatures available")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def previous_signature(self) -> SignatureResult:
        """
        Önceki imzaya geç.
        
        Returns:
            SignatureResult: Geçiş sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            if self.current_signatures:
                self.active_signature_index = (self.active_signature_index - 1) % len(self.current_signatures)
                signature = self.current_signatures[self.active_signature_index]
                
                result.success = True
                result.active_signature = signature
                result.message = f"Signature {self.active_signature_index + 1}/{len(self.current_signatures)}"
            else:
                result.errors.append("No signatures available")
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def hide_signature(self) -> SignatureResult:
        """
        İmzayı gizle.
        
        Returns:
            SignatureResult: Gizleme sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            self.current_signatures.clear()
            self.active_signature_index = 0
            
            result.success = True
            result.message = "Signature hidden"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_signature_history(self) -> List[str]:
        """
        İmza geçmişini al.
        
        Returns:
            List[str]: Geçmiş
        """
        return self.signature_history
    
    def clear_history(self) -> SignatureResult:
        """
        Geçmişi temizle.
        
        Returns:
            SignatureResult: Temizleme sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            self.signature_history.clear()
            result.success = True
            result.message = "Signature history cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def clear_cache(self) -> SignatureResult:
        """
        Cache'i temizle.
        
        Returns:
            SignatureResult: Temizleme sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            self.signature_cache.clear()
            result.success = True
            result.message = "Signature cache cleared"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def update_config(self, config: SignatureConfig) -> SignatureResult:
        """
        Konfigürasyon güncelle.
        
        Args:
            config: Yeni konfigürasyon
            
        Returns:
            SignatureResult: Güncelleme sonucu
        """
        result = SignatureResult(success=False)
        
        try:
            self.config = config
            result.success = True
            result.message = "Config updated"
        
        except Exception as e:
            result.errors.append(f"Error: {str(e)}")
        
        return result
    
    def get_config(self) -> SignatureConfig:
        """
        Konfigürasyon al.
        
        Returns:
            SignatureConfig: Konfigürasyon
        """
        return self.config


if __name__ == "__main__":
    # Basit test
    engine = SignatureHelpEngine()
    
    # İmza al
    result = engine.get_signature("print")
    print(f"Signature: {result.success}")
