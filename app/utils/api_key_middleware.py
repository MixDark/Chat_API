"""
Middleware de autenticación con API Keys.
Proporciona decorador para proteger endpoints.
"""
from functools import wraps
from flask import request, jsonify
from app.services.api_key_service import validate_api_key


def require_api_key(f):
    """
    Decorador que requiere una API Key válida en el header X-API-Key.
    
    Usage:
        @app.route('/protected')
        @require_api_key
        def protected_route():
            return {'data': 'secret'}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'status': 'error',
                'error': {
                    'code': 'MISSING_API_KEY',
                    'message': 'API Key requerida en header X-API-Key'
                }
            }), 401
        
        api_key_obj = validate_api_key(api_key)
        
        if not api_key_obj:
            return jsonify({
                'status': 'error',
                'error': {
                    'code': 'INVALID_API_KEY',
                    'message': 'API Key inválida o revocada'
                }
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def optional_api_key(f):
    """
    Decorador que permite pero no requiere API Key.
    Útil para período de transición.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if api_key:
            validate_api_key(api_key)
        
        return f(*args, **kwargs)
    
    return decorated_function
