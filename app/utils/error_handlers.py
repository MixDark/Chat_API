"""
Manejadores de errores para la aplicación Flask.
Maneja todos los errores HTTP y excepciones personalizadas.
"""
from flask import jsonify
from app.utils.validators import ValidationError


def register_error_handlers(app):
    """
    Registra los manejadores de errores con la aplicación Flask.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Maneja errores de validación."""
        response = {
            'status': 'error',
            'error': error.to_dict()
        }
        return jsonify(response), 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Maneja errores 404."""
        response = {
            'status': 'error',
            'error': {
                'code': 'NOT_FOUND',
                'message': 'El recurso solicitado no fue encontrado'
            }
        }
        return jsonify(response), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Maneja errores 405."""
        response = {
            'status': 'error',
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': 'Método HTTP no permitido para este endpoint'
            }
        }
        return jsonify(response), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Maneja errores 500."""
        response = {
            'status': 'error',
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Error interno del servidor'
            }
        }
        return jsonify(response), 500
    
    @app.errorhandler(429)
    def handle_rate_limit_exceeded(error):
        """Maneja errores 429 de rate limiting."""
        response = {
            'status': 'error',
            'error': {
                'code': 'RATE_LIMIT_EXCEEDED',
                'message': 'Demasiadas solicitudes. Por favor intenta más tarde.'
            }
        }
        return jsonify(response), 429
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Maneja errores inesperados."""
        # Log the error (in production, use proper logging)
        print(f"Unexpected error: {str(error)}")
        
        response = {
            'status': 'error',
            'error': {
                'code': 'INTERNAL_SERVER_ERROR',
                'message': 'Error interno del servidor'
            }
        }
        return jsonify(response), 500
