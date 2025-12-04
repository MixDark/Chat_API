"""
Factory de aplicación Flask.
Crea y configura la instancia de la aplicación.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import config

db = SQLAlchemy()
socketio = SocketIO()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)


def create_app(config_name='default'):
    """
    Función factory para crear la aplicación.
    
    Args:
        config_name: Nombre de configuración ('development', 'testing', 'production')
        
    Returns:
        Instancia de Flask configurada
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    limiter.init_app(app)
    
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    from app.websocket_handlers import register_websocket_handlers
    register_websocket_handlers(socketio)
    
    with app.app_context():
        db.create_all()
    
    return app
