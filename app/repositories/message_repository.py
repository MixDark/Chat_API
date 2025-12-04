"""
Repositorio de mensajes para operaciones de base de datos.
Maneja todas las interacciones con la base de datos para mensajes.
"""
from app import db
from app.models import Message
from sqlalchemy.exc import IntegrityError
from app.utils.validators import ValidationError


class MessageRepository:
    """Repositorio para operaciones de base de datos de mensajes."""
    
    def save_message(self, message_data):
        """
        Guarda un mensaje en la base de datos.
        
        Args:
            message_data: Diccionario con los datos del mensaje
            
        Returns:
            Objeto Message guardado
            
        Raises:
            ValidationError: Si el message_id ya existe
        """
        try:
            message = Message(
                message_id=message_data['message_id'],
                session_id=message_data['session_id'],
                content=message_data['content'],
                timestamp=message_data['timestamp'],
                sender=message_data['sender'],
                word_count=message_data['word_count'],
                character_count=message_data['character_count'],
                processed_at=message_data['processed_at']
            )
            
            db.session.add(message)
            db.session.commit()
            
            return message
            
        except IntegrityError:
            db.session.rollback()
            raise ValidationError(
                'DUPLICATE_MESSAGE_ID',
                f'Ya existe un mensaje con el ID "{message_data["message_id"]}"',
                {'field': 'message_id'}
            )
    
    def get_messages_by_session(self, session_id, limit=10, offset=0, sender=None):
        """
        Recupera mensajes de una sesión con paginación y filtrado.
        
        Args:
            session_id: Identificador de sesión
            limit: Número máximo de mensajes a retornar
            offset: Número de mensajes a omitir
            sender: Filtro opcional por remitente ('user' o 'system')
            
        Returns:
            Lista de objetos Message
        """
        query = Message.query.filter_by(session_id=session_id)
        
        # Aplicar filtro de sender si se proporciona
        if sender:
            query = query.filter_by(sender=sender)
        
        # Aplicar paginación
        messages = query.order_by(Message.id.asc()).limit(limit).offset(offset).all()
        
        return messages
    
    def get_message_count_by_session(self, session_id, sender=None):
        """
        Obtiene el conteo total de mensajes para una sesión.
        
        Args:
            session_id: Identificador de sesión
            sender: Filtro opcional por remitente
            
        Returns:
            Conteo total de mensajes
        """
        query = Message.query.filter_by(session_id=session_id)
        
        if sender:
            query = query.filter_by(sender=sender)
        
        return query.count()
    
    def search_messages(self, session_id, filters, limit=10, offset=0):
        """
        Busca mensajes con múltiples filtros.
        
        Args:
            session_id: Identificador de sesión
            filters: Diccionario con filtros (query, start_date, end_date, sender)
            limit: Número máximo de resultados
            offset: Número de resultados a omitir
            
        Returns:
            Lista de objetos Message
        """
        query = Message.query.filter_by(session_id=session_id)
        
        if filters.get('query'):
            query = query.filter(Message.content.like(f"%{filters['query']}%"))
        
        if filters.get('start_date'):
            query = query.filter(Message.timestamp >= filters['start_date'])
        
        if filters.get('end_date'):
            query = query.filter(Message.timestamp <= filters['end_date'])
        
        if filters.get('sender'):
            query = query.filter_by(sender=filters['sender'])
        
        messages = query.order_by(Message.id.asc()).limit(limit).offset(offset).all()
        
        return messages
    
    def count_search_results(self, session_id, filters):
        """
        Cuenta los resultados de búsqueda.
        
        Args:
            session_id: Identificador de sesión
            filters: Diccionario con filtros
            
        Returns:
            Conteo total de resultados
        """
        query = Message.query.filter_by(session_id=session_id)
        
        if filters.get('query'):
            query = query.filter(Message.content.like(f"%{filters['query']}%"))
        
        if filters.get('start_date'):
            query = query.filter(Message.timestamp >= filters['start_date'])
        
        if filters.get('end_date'):
            query = query.filter(Message.timestamp <= filters['end_date'])
        
        if filters.get('sender'):
            query = query.filter_by(sender=filters['sender'])
        
        return query.count()
