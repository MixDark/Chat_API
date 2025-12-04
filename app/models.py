"""
Modelos de base de datos para la API de Chat.
Define el modelo Message con todos los campos requeridos.
"""
from datetime import datetime, timezone
from app import db


class Message(db.Model):
    """
    Modelo Message que representa un mensaje de chat.
    
    Atributos:
        id: Clave primaria auto-incremental
        message_id: Identificador único del mensaje (del cliente)
        session_id: Identificador de sesión para agrupar mensajes
        content: Contenido del mensaje
        timestamp: Cuándo se creó el mensaje (formato ISO)
        sender: Quién envió el mensaje ('user' o 'system')
        word_count: Número de palabras en el mensaje
        character_count: Número de caracteres en el mensaje
        processed_at: Cuándo fue procesado el mensaje por el servidor
    """
    
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    sender = db.Column(db.String(20), nullable=False)
    word_count = db.Column(db.Integer, nullable=False)
    character_count = db.Column(db.Integer, nullable=False)
    processed_at = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f'<Message {self.message_id} from {self.sender}>'
    
    def to_dict(self):
        """
        Convierte el mensaje a diccionario para serialización JSON.
        
        Returns:
            Representación del mensaje como diccionario
        """
        return {
            'message_id': self.message_id,
            'session_id': self.session_id,
            'content': self.content,
            'timestamp': self.timestamp,
            'sender': self.sender,
            'metadata': {
                'word_count': self.word_count,
                'character_count': self.character_count,
                'processed_at': self.processed_at
            }
        }


class APIKey(db.Model):
    """
    Modelo APIKey para autenticación de clientes.
    
    Atributos:
        id: Clave primaria auto-incremental
        key_hash: Hash SHA-256 de la API Key
        name: Nombre descriptivo de la API Key
        created_at: Fecha de creación
        last_used_at: Última vez que se usó la key
        is_active: Si la key está activa o revocada
    """
    
    __tablename__ = 'api_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    key_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    last_used_at = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return f'<APIKey {self.name} ({"active" if self.is_active else "revoked"})>'
    
    def to_dict(self):
        """
        Convierte la API Key a diccionario para serialización JSON.
        No incluye el hash por seguridad.
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() + 'Z',
            'last_used_at': self.last_used_at.isoformat() + 'Z' if self.last_used_at else None,
            'is_active': self.is_active
        }
