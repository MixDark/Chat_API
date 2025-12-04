"""
Handlers de WebSocket para actualizaciones en tiempo real.
Gestiona conexiones y emisión de eventos.
"""
from flask_socketio import emit, join_room, leave_room


def register_websocket_handlers(socketio):
    """
    Registra todos los handlers de WebSocket.
    
    Args:
        socketio: Instancia de SocketIO
    """
    
    @socketio.on('connect')
    def handle_connect():
        """Cliente conectado al WebSocket."""
        emit('connected', {'message': 'Conectado al servidor WebSocket'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Cliente desconectado del WebSocket."""
        pass
    
    @socketio.on('join')
    def handle_join(data):
        """
        Cliente se une a un room de sesión.
        
        Args:
            data: {'session_id': 'session-123'}
        """
        session_id = data.get('session_id')
        if session_id:
            join_room(session_id)
            emit('joined', {'session_id': session_id})
    
    @socketio.on('leave')
    def handle_leave(data):
        """
        Cliente sale de un room de sesión.
        
        Args:
            data: {'session_id': 'session-123'}
        """
        session_id = data.get('session_id')
        if session_id:
            leave_room(session_id)
            emit('left', {'session_id': session_id})


def emit_new_message(socketio, session_id, message_data):
    """
    Emite un nuevo mensaje a todos los clientes en el room de la sesión.
    
    Args:
        socketio: Instancia de SocketIO
        session_id: ID de la sesión
        message_data: Datos del mensaje
    """
    socketio.emit('new_message', message_data, room=session_id)
