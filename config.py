"""
Módulo de configuración para la aplicación Chat API.
Maneja diferentes configuraciones de entorno (development, testing, production).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    """Clase de configuración base con ajustes comunes."""
    
    # IMPORTANTE: En producción, SIEMPRE establecer SECRET_KEY como variable de entorno
    # Nunca usar el valor por defecto en producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True


class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo."""
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR / "chat_dev.db"}'
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    """Configuración para entorno de pruebas."""
    
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """Configuración para entorno de producción."""
    
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{BASE_DIR / "chat_prod.db"}'
    SQLALCHEMY_ECHO = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
