"""
Pruebas de integración para endpoints de la API.
Prueba el ciclo completo de solicitud/respuesta.
"""
import json
import pytest


class TestMessagesEndpoint:
    """Casos de prueba para el endpoint POST /api/messages."""
    
    def test_create_message_success(self, client, sample_message):
        """Prueba la creación exitosa de un mensaje."""
        response = client.post(
            '/api/messages',
            data=json.dumps(sample_message),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert data['status'] == 'success'
        assert 'data' in data
        assert data['data']['message_id'] == sample_message['message_id']
        assert data['data']['session_id'] == sample_message['session_id']
        assert data['data']['content'] == sample_message['content']
        assert data['data']['sender'] == sample_message['sender']
        assert 'metadata' in data['data']
        assert 'word_count' in data['data']['metadata']
        assert 'character_count' in data['data']['metadata']
        assert 'processed_at' in data['data']['metadata']
    
    def test_create_message_missing_fields(self, client):
        """Prueba que la creación de mensaje falla con campos faltantes."""
        invalid_message = {
            'message_id': 'msg-123',
            'content': 'Hello'
        }
        
        response = client.post(
            '/api/messages',
            data=json.dumps(invalid_message),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['status'] == 'error'
        assert 'error' in data
        assert data['error']['code'] == 'MISSING_FIELDS'
    
    def test_create_message_invalid_sender(self, client, sample_message):
        """Prueba que la creación de mensaje falla con sender inválido."""
        sample_message['sender'] = 'invalid'
        
        response = client.post(
            '/api/messages',
            data=json.dumps(sample_message),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['status'] == 'error'
        assert data['error']['code'] == 'INVALID_SENDER'
    
    def test_create_message_invalid_timestamp(self, client, sample_message):
        """Prueba que la creación de mensaje falla con timestamp inválido."""
        sample_message['timestamp'] = 'not-a-timestamp'
        
        response = client.post(
            '/api/messages',
            data=json.dumps(sample_message),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['status'] == 'error'
        assert data['error']['code'] == 'INVALID_TIMESTAMP'
    
    def test_create_message_duplicate_id(self, client, sample_message):
        """Prueba que la creación de mensaje falla con message_id duplicado."""
        # Crear primer mensaje
        client.post(
            '/api/messages',
            data=json.dumps(sample_message),
            content_type='application/json'
        )
        
        # Intentar crear duplicado
        response = client.post(
            '/api/messages',
            data=json.dumps(sample_message),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['status'] == 'error'
        assert data['error']['code'] == 'DUPLICATE_MESSAGE_ID'
    
    def test_create_message_content_filtering(self, client, sample_message):
        """Prueba que las palabras prohibidas son filtradas del contenido."""
        sample_message['content'] = 'This is spam and a scam'
        
        response = client.post(
            '/api/messages',
            data=json.dumps(sample_message),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        # Verificar que las palabras prohibidas son filtradas
        assert 'spam' not in data['data']['content']
        assert 'scam' not in data['data']['content']
        assert '****' in data['data']['content']


class TestGetMessagesEndpoint:
    """Casos de prueba para el endpoint GET /api/messages/<session_id>."""
    
    def test_get_messages_success(self, client, sample_message, sample_user_message):
        """Prueba la recuperación exitosa de mensajes."""
        # Crear dos mensajes
        client.post('/api/messages', data=json.dumps(sample_message), content_type='application/json')
        client.post('/api/messages', data=json.dumps(sample_user_message), content_type='application/json')
        
        # Obtener mensajes
        response = client.get('/api/messages/session-abcdef')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'success'
        assert 'data' in data
        assert len(data['data']) == 2
        assert 'pagination' in data
        assert data['pagination']['total'] == 2
    
    def test_get_messages_with_pagination(self, client, sample_message):
        """Prueba la recuperación de mensajes con paginación."""
        # Crear múltiples mensajes
        for i in range(5):
            msg = sample_message.copy()
            msg['message_id'] = f'msg-{i}'
            client.post('/api/messages', data=json.dumps(msg), content_type='application/json')
        
        # Obtener primeros 2 mensajes
        response = client.get('/api/messages/session-abcdef?limit=2&offset=0')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) == 2
        assert data['pagination']['limit'] == 2
        assert data['pagination']['offset'] == 0
        assert data['pagination']['total'] == 5
    
    def test_get_messages_with_sender_filter(self, client, sample_message, sample_user_message):
        """Prueba la recuperación de mensajes con filtro de remitente."""
        # Crear mensajes de diferentes remitentes
        client.post('/api/messages', data=json.dumps(sample_message), content_type='application/json')
        client.post('/api/messages', data=json.dumps(sample_user_message), content_type='application/json')
        
        # Obtener solo mensajes de usuario
        response = client.get('/api/messages/session-abcdef?sender=user')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) == 1
        assert data['data'][0]['sender'] == 'user'
        assert data['pagination']['total'] == 1
    
    def test_get_messages_invalid_sender_filter(self, client):
        """Prueba que la recuperación de mensajes falla con filtro de sender inválido."""
        response = client.get('/api/messages/session-abcdef?sender=invalid')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        
        assert data['status'] == 'error'
        assert data['error']['code'] == 'INVALID_SENDER'
    
    def test_get_messages_empty_session(self, client):
        """Prueba la recuperación de mensajes de una sesión inexistente."""
        response = client.get('/api/messages/non-existent-session')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'success'
        assert len(data['data']) == 0
        assert data['pagination']['total'] == 0


class TestHealthEndpoint:
    """Casos de prueba para el endpoint de verificación de salud."""
    
    def test_health_check(self, client):
        """Prueba el endpoint de verificación de salud."""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'healthy'
        assert data['message'] == 'API is running'


class TestErrorHandling:
    """Casos de prueba para el manejo de errores."""
    
    def test_404_error(self, client):
        """Prueba el manejo de errores 404."""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        
        assert data['status'] == 'error'
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_405_error(self, client):
        """Prueba el manejo de errores 405."""
        response = client.put('/api/messages')
        
        assert response.status_code == 405
        data = json.loads(response.data)
        
        assert data['status'] == 'error'
        assert data['error']['code'] == 'METHOD_NOT_ALLOWED'
