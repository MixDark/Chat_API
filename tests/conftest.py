"""
Configuración de Pytest y fixtures.
Provee fixtures de prueba para la suite de tests.
"""
import pytest
from app import create_app, db


@pytest.fixture
def app():
    """
    Crea y configura una instancia de aplicación de prueba.
    
    Yields:
        Aplicación Flask configurada para pruebas
    """
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Crea un cliente de prueba para la aplicación.
    
    Args:
        app: Fixture de aplicación Flask
        
    Returns:
        Cliente de prueba Flask
    """
    return app.test_client()


@pytest.fixture
def sample_message():
    """
    Proporciona datos de mensaje de ejemplo para las pruebas.
    
    Returns:
        Diccionario con datos de mensaje válidos
    """
    return {
        'message_id': 'msg-123456',
        'session_id': 'session-abcdef',
        'content': 'Hola, ¿cómo puedo ayudarte hoy?',
        'timestamp': '2023-06-15T14:30:00Z',
        'sender': 'system'
    }


@pytest.fixture
def sample_user_message():
    """
    Proporciona datos de mensaje de usuario de ejemplo para las pruebas.
    
    Returns:
        Diccionario con datos de mensaje de usuario válidos
    """
    return {
        'message_id': 'msg-789012',
        'session_id': 'session-abcdef',
        'content': 'Necesito ayuda con mi cuenta',
        'timestamp': '2023-06-15T14:31:00Z',
        'sender': 'user'
    }


@pytest.fixture
def socketio(app):
    """
    Proporciona instancia de SocketIO para tests.
    
    Args:
        app: Fixture de aplicación Flask
        
    Returns:
        Instancia de SocketIO
    """
    from app import socketio
    return socketio
