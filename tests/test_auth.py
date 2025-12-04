"""
Tests para el sistema de autenticación con API Keys.
"""
import pytest
from app.services.api_key_service import (
    generate_api_key,
    hash_api_key,
    create_api_key,
    validate_api_key,
    revoke_api_key,
    list_api_keys
)
from app.models import APIKey


class TestAPIKeyGeneration:
    """Tests para generación de API Keys."""
    
    def test_generate_api_key_length(self):
        """Verifica que la API Key generada tenga 64 caracteres."""
        api_key = generate_api_key()
        assert len(api_key) == 64
    
    def test_generate_api_key_uniqueness(self):
        """Verifica que cada API Key generada sea única."""
        key1 = generate_api_key()
        key2 = generate_api_key()
        assert key1 != key2
    
    def test_hash_api_key(self):
        """Verifica que el hash sea consistente y tenga 64 caracteres."""
        api_key = "test-key-123"
        hash1 = hash_api_key(api_key)
        hash2 = hash_api_key(api_key)
        
        assert hash1 == hash2
        assert len(hash1) == 64


class TestAPIKeyCreation:
    """Tests para creación de API Keys."""
    
    def test_create_api_key_success(self, app):
        """Verifica que se pueda crear una API Key correctamente."""
        with app.app_context():
            api_key_plain, api_key_obj = create_api_key("Test Key")
            
            assert len(api_key_plain) == 64
            assert api_key_obj.name == "Test Key"
            assert api_key_obj.is_active is True
            assert api_key_obj.id is not None
    
    def test_create_api_key_stored_as_hash(self, app):
        """Verifica que la API Key se almacene como hash."""
        with app.app_context():
            api_key_plain, api_key_obj = create_api_key("Test Key")
            
            assert api_key_obj.key_hash != api_key_plain
            assert len(api_key_obj.key_hash) == 64


class TestAPIKeyValidation:
    """Tests para validación de API Keys."""
    
    def test_validate_api_key_success(self, app):
        """Verifica que una API Key válida sea aceptada."""
        with app.app_context():
            api_key_plain, api_key_obj = create_api_key("Test Key")
            
            validated = validate_api_key(api_key_plain)
            
            assert validated is not None
            assert validated.id == api_key_obj.id
            assert validated.last_used_at is not None
    
    def test_validate_api_key_invalid(self, app):
        """Verifica que una API Key inválida sea rechazada."""
        with app.app_context():
            validated = validate_api_key("invalid-key-123")
            assert validated is None
    
    def test_validate_api_key_revoked(self, app):
        """Verifica que una API Key revocada sea rechazada."""
        with app.app_context():
            api_key_plain, api_key_obj = create_api_key("Test Key")
            revoke_api_key(api_key_obj.id)
            
            validated = validate_api_key(api_key_plain)
            assert validated is None
    
    def test_validate_api_key_empty(self, app):
        """Verifica que una API Key vacía sea rechazada."""
        with app.app_context():
            validated = validate_api_key("")
            assert validated is None
    
    def test_validate_api_key_none(self, app):
        """Verifica que None sea rechazado."""
        with app.app_context():
            validated = validate_api_key(None)
            assert validated is None


class TestAPIKeyRevocation:
    """Tests para revocación de API Keys."""
    
    def test_revoke_api_key_success(self, app):
        """Verifica que se pueda revocar una API Key."""
        with app.app_context():
            _, api_key_obj = create_api_key("Test Key")
            
            result = revoke_api_key(api_key_obj.id)
            
            assert result is True
            
            revoked_key = APIKey.query.get(api_key_obj.id)
            assert revoked_key.is_active is False
    
    def test_revoke_api_key_nonexistent(self, app):
        """Verifica que revocar una API Key inexistente retorne False."""
        with app.app_context():
            result = revoke_api_key(99999)
            assert result is False


class TestAPIKeyListing:
    """Tests para listado de API Keys."""
    
    def test_list_api_keys_empty(self, app):
        """Verifica que el listado esté vacío inicialmente."""
        with app.app_context():
            keys = list_api_keys()
            assert len(keys) == 0
    
    def test_list_api_keys_multiple(self, app):
        """Verifica que se listen todas las API Keys."""
        with app.app_context():
            create_api_key("Key 1")
            create_api_key("Key 2")
            create_api_key("Key 3")
            
            keys = list_api_keys()
            assert len(keys) == 3
    
    def test_list_api_keys_includes_revoked(self, app):
        """Verifica que el listado incluya API Keys revocadas."""
        with app.app_context():
            _, key1 = create_api_key("Key 1")
            _, key2 = create_api_key("Key 2")
            
            revoke_api_key(key1.id)
            
            keys = list_api_keys()
            assert len(keys) == 2
