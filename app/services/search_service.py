"""
Servicio de búsqueda de mensajes.
Permite buscar mensajes por contenido y filtros.
"""
from app.repositories.message_repository import MessageRepository


def search_messages(session_id, query='', start_date=None, end_date=None, sender=None, limit=10, offset=0):
    """
    Busca mensajes en una sesión con múltiples filtros.
    
    Args:
        session_id: ID de la sesión
        query: Texto a buscar en el contenido
        start_date: Fecha de inicio (ISO 8601)
        end_date: Fecha de fin (ISO 8601)
        sender: Filtrar por remitente
        limit: Número máximo de resultados
        offset: Número de resultados a omitir
        
    Returns:
        Tupla (lista de mensajes, total de resultados)
    """
    repository = MessageRepository()
    
    filters = {
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'sender': sender
    }
    
    messages = repository.search_messages(session_id, filters, limit, offset)
    total = repository.count_search_results(session_id, filters)
    
    return [msg.to_dict() for msg in messages], total
