"""
Servicio de autenticación con API Keys.
Maneja la generación, validación y gestión de API Keys.
"""
import secrets
import hashlib
from datetime import datetime, timezone
from app import db
from app.models import APIKey


def generate_api_key():
    """
    Genera una nueva API Key segura.
    
    Returns:
        String de 32 caracteres hexadecimales
    """
    return secrets.token_hex(32)


def hash_api_key(api_key):
    """
    Genera hash SHA-256 de una API Key.
    
    Args:
        api_key: API Key en texto plano
        
    Returns:
        Hash SHA-256 en hexadecimal
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def create_api_key(name):
    """
    Crea una nueva API Key en la base de datos.
    
    Args:
        name: Nombre descriptivo para la API Key
        
    Returns:
        Tupla (api_key_plain, api_key_object)
    """
    api_key_plain = generate_api_key()
    key_hash = hash_api_key(api_key_plain)
    
    api_key = APIKey(
        key_hash=key_hash,
        name=name,
        is_active=True
    )
    
    db.session.add(api_key)
    db.session.commit()
    
    return api_key_plain, api_key


def validate_api_key(api_key):
    """
    Valida una API Key y actualiza last_used_at.
    
    Args:
        api_key: API Key en texto plano
        
    Returns:
        APIKey object si es válida, None si no
    """
    if not api_key:
        return None
    
    key_hash = hash_api_key(api_key)
    api_key_obj = APIKey.query.filter_by(key_hash=key_hash, is_active=True).first()
    
    if api_key_obj:
        api_key_obj.last_used_at = datetime.now(timezone.utc)
        db.session.commit()
    
    return api_key_obj


def revoke_api_key(key_id):
    """
    Revoca una API Key existente.
    
    Args:
        key_id: ID de la API Key a revocar
        
    Returns:
        True si se revocó, False si no existe
    """
    api_key = APIKey.query.get(key_id)
    if not api_key:
        return False
    
    api_key.is_active = False
    db.session.commit()
    return True


def list_api_keys():
    """
    Lista todas las API Keys.
    
    Returns:
        Lista de objetos APIKey
    """
    return APIKey.query.all()
