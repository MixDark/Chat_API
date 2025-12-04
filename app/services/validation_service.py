"""
Servicio de validación para mensajes.
Maneja toda la lógica de validación para mensajes entrantes.
"""
from datetime import datetime
from dateutil import parser
from app.utils.validators import ValidationError


class ValidationService:
    """Servicio para validar datos de mensajes."""
    
    REQUIRED_FIELDS = ['message_id', 'session_id', 'content', 'timestamp', 'sender']
    VALID_SENDERS = ['user', 'system']
    
    @staticmethod
    def validate_message(data):
        """
        Valida los datos del mensaje.
        
        Args:
            data: Diccionario con los datos del mensaje
            
        Raises:
            ValidationError: Si la validación falla
            
        Returns:
            True si la validación es exitosa
        """
        if not isinstance(data, dict):
            raise ValidationError('INVALID_FORMAT', 'El cuerpo de la solicitud debe ser un objeto JSON')
        
        ValidationService._validate_required_fields(data)
        ValidationService._validate_field_types(data)
        ValidationService._validate_timestamp(data['timestamp'])
        ValidationService._validate_sender(data['sender'])
        ValidationService._validate_content(data['content'])
        
        return True
    
    @staticmethod
    def _validate_required_fields(data):
        """Verifica que todos los campos requeridos estén presentes."""
        missing_fields = [field for field in ValidationService.REQUIRED_FIELDS if field not in data]
        
        if missing_fields:
            raise ValidationError(
                'MISSING_FIELDS',
                f'Faltan campos requeridos: {", ".join(missing_fields)}',
                {'missing_fields': missing_fields}
            )
    
    @staticmethod
    def _validate_field_types(data):
        """Valida que los campos tengan los tipos correctos."""
        string_fields = ['message_id', 'session_id', 'content', 'timestamp', 'sender']
        
        for field in string_fields:
            if field in data and not isinstance(data[field], str):
                raise ValidationError(
                    'INVALID_TYPE',
                    f'El campo "{field}" debe ser una cadena de texto',
                    {'field': field, 'expected_type': 'string'}
                )
    
    @staticmethod
    def _validate_timestamp(timestamp):
        """Valida que el timestamp esté en formato ISO."""
        try:
            parser.isoparse(timestamp)
        except (ValueError, TypeError):
            raise ValidationError(
                'INVALID_TIMESTAMP',
                'El campo "timestamp" debe estar en formato ISO datetime (ej: 2023-06-15T14:30:00Z)',
                {'field': 'timestamp', 'expected_format': 'ISO 8601'}
            )
    
    @staticmethod
    def _validate_sender(sender):
        """Valida que el sender sea 'user' o 'system'."""
        if sender not in ValidationService.VALID_SENDERS:
            raise ValidationError(
                'INVALID_SENDER',
                f'El campo "sender" debe ser "user" o "system"',
                {'field': 'sender', 'valid_values': ValidationService.VALID_SENDERS}
            )
    
    @staticmethod
    def _validate_content(content):
        """Valida que el contenido no esté vacío."""
        if not content or not content.strip():
            raise ValidationError(
                'EMPTY_CONTENT',
                'El campo "content" no puede estar vacío',
                {'field': 'content'}
            )
