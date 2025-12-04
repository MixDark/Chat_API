"""
Validadores personalizados y excepciones.
"""


class ValidationError(Exception):
    """Excepción personalizada para errores de validación."""
    
    def __init__(self, code, message, details=None):
        """
        Inicializa el error de validación.
        
        Args:
            code: Código de error (ej: 'INVALID_FORMAT')
            message: Mensaje de error legible
            details: Detalles adicionales opcionales
        """
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self):
        """Convierte el error a diccionario para respuesta JSON."""
        error_dict = {
            'code': self.code,
            'message': self.message
        }
        
        if self.details:
            error_dict['details'] = self.details
        
        return error_dict
