"""
Pruebas unitarias para servicios.
Prueba el servicio de validación y el servicio de mensajes.
"""
import pytest
from app.services.validation_service import ValidationService
from app.services.message_service import MessageService
from app.utils.validators import ValidationError


class TestValidationService:
    """Casos de prueba para ValidationService."""
    
    def test_validate_valid_message(self, sample_message):
        """Prueba la validación de un mensaje válido."""
        result = ValidationService.validate_message(sample_message)
        assert result is True
    
    def test_validate_missing_fields(self):
        """Prueba que la validación falla con campos faltantes."""
        invalid_data = {
            'message_id': 'msg-123',
            'content': 'Hello'
        }
        
        with pytest.raises(ValidationError) as exc_info:
            ValidationService.validate_message(invalid_data)
        
        assert exc_info.value.code == 'MISSING_FIELDS'
        assert 'session_id' in str(exc_info.value.message)
    
    def test_validate_invalid_sender(self, sample_message):
        """Prueba que la validación falla con sender inválido."""
        sample_message['sender'] = 'invalid'
        
        with pytest.raises(ValidationError) as exc_info:
            ValidationService.validate_message(sample_message)
        
        assert exc_info.value.code == 'INVALID_SENDER'
    
    def test_validate_invalid_timestamp(self, sample_message):
        """Prueba que la validación falla con formato de timestamp inválido."""
        sample_message['timestamp'] = 'not-a-timestamp'
        
        with pytest.raises(ValidationError) as exc_info:
            ValidationService.validate_message(sample_message)
        
        assert exc_info.value.code == 'INVALID_TIMESTAMP'
    
    def test_validate_empty_content(self, sample_message):
        """Prueba que la validación falla con contenido vacío."""
        sample_message['content'] = '   '
        
        with pytest.raises(ValidationError) as exc_info:
            ValidationService.validate_message(sample_message)
        
        assert exc_info.value.code == 'EMPTY_CONTENT'
    
    def test_validate_invalid_type(self, sample_message):
        """Prueba que la validación falla con tipo de campo inválido."""
        sample_message['message_id'] = 12345  # Should be string
        
        with pytest.raises(ValidationError) as exc_info:
            ValidationService.validate_message(sample_message)
        
        assert exc_info.value.code == 'INVALID_TYPE'
    
    def test_validate_not_dict(self):
        """Prueba que la validación falla cuando los datos no son un diccionario."""
        with pytest.raises(ValidationError) as exc_info:
            ValidationService.validate_message("not a dict")
        
        assert exc_info.value.code == 'INVALID_FORMAT'


class TestMessageService:
    """Casos de prueba para MessageService."""
    
    def test_filter_content_with_bad_words(self):
        """Prueba que el filtrado de contenido elimina palabras prohibidas."""
        service = MessageService()
        
        content = "This is spam and a scam"
        filtered = service._filter_content(content)
        
        assert 'spam' not in filtered
        assert 'scam' not in filtered
        assert '****' in filtered
    
    def test_filter_content_case_insensitive(self):
        """Prueba que el filtrado de contenido es insensible a mayúsculas."""
        service = MessageService()
        
        content = "This is SPAM and Scam"
        filtered = service._filter_content(content)
        
        assert 'SPAM' not in filtered
        assert 'Scam' not in filtered
    
    def test_generate_metadata(self):
        """Prueba la generación de metadata."""
        service = MessageService()
        
        content = "Hola, ¿cómo estás?"
        metadata = service._generate_metadata(content)
        
        assert metadata['word_count'] == 3  # "Hola," "¿cómo" "estás?"
        assert metadata['character_count'] == len(content)
        assert 'processed_at' in metadata
        assert 'T' in metadata['processed_at']  # ISO format
        assert 'Z' in metadata['processed_at']
    
    def test_generate_metadata_empty_content(self):
        """Prueba la generación de metadata con contenido vacío."""
        service = MessageService()
        
        content = ""
        metadata = service._generate_metadata(content)
        
        assert metadata['word_count'] == 0
        assert metadata['character_count'] == 0
