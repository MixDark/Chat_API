"""
Servicio de procesamiento de mensajes.
Maneja el pipeline de procesamiento incluyendo filtrado y generación de metadata.
"""
from datetime import datetime, timezone
from app.services.validation_service import ValidationService
from app.repositories.message_repository import MessageRepository


class MessageService:
    """Servicio para procesar y gestionar mensajes."""
    
    # Lista de palabras prohibidas para filtrado de contenido
    BAD_WORDS = ['spam', 'malware', 'phishing', 'scam']
    
    def __init__(self):
        """Inicializa el servicio de mensajes."""
        self.validation_service = ValidationService()
        self.repository = MessageRepository()
    
    def process_and_save_message(self, data):
        """
        Procesa y guarda un mensaje.
        
        Args:
            data: Diccionario con los datos del mensaje
            
        Returns:
            Diccionario con los datos del mensaje procesado
        """
        self.validation_service.validate_message(data)
        processed_content = self._filter_content(data['content'])
        metadata = self._generate_metadata(processed_content)
        
        message_data = {
            'message_id': data['message_id'],
            'session_id': data['session_id'],
            'content': processed_content,
            'timestamp': data['timestamp'],
            'sender': data['sender'],
            'word_count': metadata['word_count'],
            'character_count': metadata['character_count'],
            'processed_at': metadata['processed_at']
        }
        
        message = self.repository.save_message(message_data)
        message_dict = message.to_dict()
        
        # Emitir mensaje via WebSocket a todos los clientes en el room
        from app import socketio
        from app.websocket_handlers import emit_new_message
        emit_new_message(socketio, data['session_id'], message_dict)
        
        return message_dict
    
    def get_messages_by_session(self, session_id, limit=10, offset=0, sender=None):
        """
        Recupera mensajes de una sesión.
        
        Args:
            session_id: Identificador de sesión
            limit: Número máximo de mensajes a retornar
            offset: Número de mensajes a omitir
            sender: Filtro opcional por remitente
            
        Returns:
            Lista de diccionarios de mensajes
        """
        messages = self.repository.get_messages_by_session(
            session_id=session_id,
            limit=limit,
            offset=offset,
            sender=sender
        )
        
        return [msg.to_dict() for msg in messages]
    
    def _filter_content(self, content):
        """
        Filtra contenido inapropiado del mensaje.
        
        Args:
            content: Contenido original del mensaje
            
        Returns:
            Contenido filtrado
        """
        filtered_content = content
        
        # Filtrado simple de palabras (insensible a mayúsculas)
        for bad_word in self.BAD_WORDS:
            # Reemplazar palabras prohibidas con asteriscos
            filtered_content = filtered_content.replace(
                bad_word, 
                '*' * len(bad_word)
            )
            filtered_content = filtered_content.replace(
                bad_word.capitalize(), 
                '*' * len(bad_word)
            )
            filtered_content = filtered_content.replace(
                bad_word.upper(), 
                '*' * len(bad_word)
            )
        
        return filtered_content
    
    def _generate_metadata(self, content):
        """
        Genera metadata para un mensaje.
        
        Args:
            content: Contenido del mensaje
            
        Returns:
            Diccionario con metadata
        """
        words = content.split()
        word_count = len(words)
        character_count = len(content)
        processed_at = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        
        return {
            'word_count': word_count,
            'character_count': character_count,
            'processed_at': processed_at
        }
