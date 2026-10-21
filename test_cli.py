"""
MuhammedAI Local Developer - CLI Testleri
main.py CLI için hızlı testler.
"""

import sys
import pytest
from unittest.mock import patch, MagicMock
from main import check_ollama_connection, check_model


def test_cli_ollama_connection_failure():
    """Ollama bağlantısı olmadığında hata döndürmeli."""
    with patch('ollama.Client') as mock_client:
        mock_client_instance = MagicMock()
        mock_client_instance.list.side_effect = Exception("Connection failed")
        mock_client.return_value = mock_client_instance
        
        result = check_ollama_connection()
        assert result is False


def test_cli_ollama_connection_success():
    """Ollama bağlantısı başarılı olduğunda True döndürmeli."""
    with patch('ollama.Client') as mock_client:
        mock_client_instance = MagicMock()
        mock_client_instance.list.return_value = {"models": []}
        mock_client.return_value = mock_client_instance
        
        result = check_ollama_connection()
        assert result is True


def test_cli_model_not_found():
    """Model bulunamazsa False döndürmeli."""
    with patch('ollama.Client') as mock_client:
        mock_client_instance = MagicMock()
        # Model objesi mock oluştur
        mock_model = MagicMock()
        mock_model.model = "other:latest"
        mock_response = MagicMock()
        mock_response.models = [mock_model]
        mock_client_instance.list.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        result = check_model(model="qwen3:4b")
        assert result is False


def test_cli_model_found():
    """Model bulunursa True döndürmeli."""
    with patch('ollama.Client') as mock_client:
        mock_client_instance = MagicMock()
        # Model objesi mock oluştur
        mock_model = MagicMock()
        mock_model.model = "qwen3:4b"
        mock_response = MagicMock()
        mock_response.models = [mock_model]
        mock_client_instance.list.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        result = check_model(model="qwen3:4b")
        assert result is True


def test_cli_approval_callback_yes():
    """Onay callback 'y' ile True döndürmeli."""
    with patch('builtins.input', return_value='y'):
        from main import approval_callback
        result = approval_callback("test_tool", {"arg": "value"})
        assert result is True


def test_cli_approval_callback_no():
    """Onay callback 'n' ile False döndürmeli."""
    with patch('builtins.input', return_value='n'):
        from main import approval_callback
        result = approval_callback("test_tool", {"arg": "value"})
        assert result is False


def test_cli_approval_callback_invalid_then_yes():
    """Geçersiz girdi sonrası 'y' ile True döndürmeli."""
    with patch('builtins.input', side_effect=['invalid', 'y']):
        from main import approval_callback
        result = approval_callback("test_tool", {"arg": "value"})
        assert result is True


def test_cli_model_empty_list():
    """Boş model listesi ile False döndürmeli."""
    with patch('ollama.Client') as mock_client:
        mock_client_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.models = []
        mock_client_instance.list.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        result = check_model(model="qwen3:4b")
        assert result is False


def test_cli_model_with_tag():
    """Model tag ile eşleşmeli (qwen3:4b)."""
    with patch('ollama.Client') as mock_client:
        mock_client_instance = MagicMock()
        mock_model = MagicMock()
        mock_model.model = "qwen3:4b"
        mock_response = MagicMock()
        mock_response.models = [mock_model]
        mock_client_instance.list.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        result = check_model(model="qwen3:4b")
        assert result is True


def test_cli_model_without_tag():
    """Model tag olmadan da eşleşmeli (qwen3)."""
    with patch('ollama.Client') as mock_client:
        mock_client_instance = MagicMock()
        mock_model = MagicMock()
        mock_model.model = "qwen3:4b"
        mock_response = MagicMock()
        mock_response.models = [mock_model]
        mock_client_instance.list.return_value = mock_response
        mock_client.return_value = mock_client_instance
        
        result = check_model(model="qwen3")
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
