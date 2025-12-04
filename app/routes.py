"""
Rutas de la API de Chat.
Define todos los endpoints de la API.
"""
from flask import Blueprint, request, jsonify
from app.services.message_service import MessageService
from app.services.api_key_service import create_api_key, list_api_keys, revoke_api_key
from app.utils.api_key_middleware import optional_api_key
from app import limiter

api_bp = Blueprint('api', __name__, url_prefix='/api')
message_service = MessageService()


@api_bp.route('/messages', methods=['POST'])
@limiter.limit("20 per minute")
@optional_api_key
def create_message():

    data = request.get_json()
    result = message_service.process_and_save_message(data)
    
    response = {
        'status': 'success',
        'data': result
    }
    
    return jsonify(response), 201


@api_bp.route('/messages/<session_id>', methods=['GET'])
@limiter.limit("60 per minute")
@optional_api_key
def get_messages(session_id):
    """
    Recupera mensajes de una sesión.
    
    Parámetros de consulta:
        - limit: Número máximo de mensajes a retornar (por defecto: 10)
        - offset: Número de mensajes a omitir (por defecto: 0)
        - sender: Filtrar por remitente ('user' o 'system', opcional)
    """
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    sender = request.args.get('sender', default=None, type=str)
    
    # Validar parámetros de paginación
    if limit < 1 or limit > 100:
        limit = 10
    if offset < 0:
        offset = 0
    
    # Validar parámetro sender si se proporciona
    if sender and sender not in ['user', 'system']:
        from app.utils.validators import ValidationError
        raise ValidationError(
            'INVALID_SENDER',
            'El parámetro "sender" debe ser "user" o "system"',
            {'field': 'sender', 'valid_values': ['user', 'system']}
        )
    
    messages = message_service.get_messages_by_session(
        session_id=session_id,
        limit=limit,
        offset=offset,
        sender=sender
    )
    
    from app.repositories.message_repository import MessageRepository
    repository = MessageRepository()
    total = repository.get_message_count_by_session(session_id, sender)
    
    response = {
        'status': 'success',
        'data': messages,
        'pagination': {
            'limit': limit,
            'offset': offset,
            'total': total
        }
    }
    
    return jsonify(response), 200


@api_bp.route('/messages/<session_id>/search', methods=['GET'])
@limiter.limit("30 per minute")
@optional_api_key
def search_messages(session_id):
    """
    Busca mensajes en una sesión.
    
    Parámetros de consulta:
        - q: Texto a buscar en el contenido
        - start_date: Fecha de inicio (ISO 8601)
        - end_date: Fecha de fin (ISO 8601)
        - sender: Filtrar por remitente
        - limit: Número máximo de resultados
        - offset: Número de resultados a omitir
    """
    from app.services.search_service import search_messages as search_service
    
    query = request.args.get('q', default='', type=str)
    start_date = request.args.get('start_date', default=None, type=str)
    end_date = request.args.get('end_date', default=None, type=str)
    sender = request.args.get('sender', default=None, type=str)
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    results, total = search_service(
        session_id=session_id,
        query=query,
        start_date=start_date,
        end_date=end_date,
        sender=sender,
        limit=limit,
        offset=offset
    )
    
    response = {
        'status': 'success',
        'data': results,
        'pagination': {
            'limit': limit,
            'offset': offset,
            'total': total
        }
    }
    
    return jsonify(response), 200


@api_bp.route('/auth/keys', methods=['POST'])
def create_new_api_key():
    """
    Crea una nueva API Key.
    
    Body:
        - name: Nombre descriptivo para la API Key
    """
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'MISSING_FIELDS',
                'message': 'El campo "name" es requerido'
            }
        }), 400
    
    name = data['name']
    
    if not isinstance(name, str) or len(name.strip()) == 0:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'INVALID_NAME',
                'message': 'El nombre debe ser un string no vacío'
            }
        }), 400
    
    api_key_plain, api_key_obj = create_api_key(name)
    
    response = {
        'status': 'success',
        'data': {
            'api_key': api_key_plain,
            'key_info': api_key_obj.to_dict()
        },
        'message': 'Guarda esta API Key de forma segura. No se mostrará nuevamente.'
    }
    
    return jsonify(response), 201


@api_bp.route('/auth/keys', methods=['GET'])
def get_api_keys():
    """
    Lista todas las API Keys (sin mostrar las keys reales).
    """
    keys = list_api_keys()
    
    response = {
        'status': 'success',
        'data': [key.to_dict() for key in keys]
    }
    
    return jsonify(response), 200


@api_bp.route('/auth/keys/<int:key_id>', methods=['DELETE'])
def delete_api_key(key_id):
    """
    Revoca una API Key.
    """
    success = revoke_api_key(key_id)
    
    if not success:
        return jsonify({
            'status': 'error',
            'error': {
                'code': 'NOT_FOUND',
                'message': 'API Key no encontrada'
            }
        }), 404
    
    response = {
        'status': 'success',
        'message': 'API Key revocada exitosamente'
    }
    
    return jsonify(response), 200


@api_bp.route('/health', methods=['GET'])
def health_check():
    
    """Endpoint de verificación de salud."""
    
    return jsonify({
        "message": "API is running",
        "status": "healthy"
    }), 200
