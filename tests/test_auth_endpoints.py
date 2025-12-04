"""
Tests para endpoints de autenticación.
"""
import json


class TestAuthEndpoints:
    """Tests para endpoints de autenticación."""
    
    def test_create_api_key_success(self, client):
        """Verifica que se pueda crear una API Key."""
        response = client.post(
            '/api/auth/keys',
            data=json.dumps({'name': 'Test Application'}),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert data['status'] == 'success'
        assert 'api_key' in data['data']
        assert len(data['data']['api_key']) == 64
        assert data['data']['key_info']['name'] == 'Test Application'
        assert data['data']['key_info']['is_active'] is True
    
    def test_create_api_key_missing_name(self, client):
        """Verifica error cuando falta el nombre."""
        response = client.post(
            '/api/auth/keys',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert data['error']['code'] == 'MISSING_FIELDS'
    
    def test_create_api_key_empty_name(self, client):
        """Verifica error cuando el nombre está vacío."""
        response = client.post(
            '/api/auth/keys',
            data=json.dumps({'name': '   '}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert data['error']['code'] == 'INVALID_NAME'
    
    def test_create_api_key_invalid_type(self, client):
        """Verifica error cuando el nombre no es string."""
        response = client.post(
            '/api/auth/keys',
            data=json.dumps({'name': 123}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_list_api_keys_empty(self, client):
        """Verifica que el listado esté vacío inicialmente."""
        response = client.get('/api/auth/keys')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'success'
        assert len(data['data']) == 0
    
    def test_list_api_keys_with_keys(self, client):
        """Verifica que se listen las API Keys creadas."""
        client.post(
            '/api/auth/keys',
            data=json.dumps({'name': 'Key 1'}),
            content_type='application/json'
        )
        client.post(
            '/api/auth/keys',
            data=json.dumps({'name': 'Key 2'}),
            content_type='application/json'
        )
        
        response = client.get('/api/auth/keys')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert len(data['data']) == 2
        assert data['data'][0]['name'] == 'Key 1'
        assert data['data'][1]['name'] == 'Key 2'
    
    def test_revoke_api_key_success(self, client):
        """Verifica que se pueda revocar una API Key."""
        create_response = client.post(
            '/api/auth/keys',
            data=json.dumps({'name': 'Test Key'}),
            content_type='application/json'
        )
        create_data = json.loads(create_response.data)
        key_id = create_data['data']['key_info']['id']
        
        response = client.delete(f'/api/auth/keys/{key_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'revocada' in data['message']
    
    def test_revoke_api_key_nonexistent(self, client):
        """Verifica error al revocar API Key inexistente."""
        response = client.delete('/api/auth/keys/99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert data['error']['code'] == 'NOT_FOUND'
    
    def test_create_message_with_valid_api_key(self, client):
        """Verifica que se pueda crear mensaje con API Key válida."""
        create_response = client.post(
            '/api/auth/keys',
            data=json.dumps({'name': 'Test Key'}),
            content_type='application/json'
        )
        create_data = json.loads(create_response.data)
        api_key = create_data['data']['api_key']
        
        response = client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'msg-with-auth',
                'session_id': 'session-123',
                'content': 'Test message',
                'timestamp': '2025-12-04T15:00:00Z',
                'sender': 'user'
            }),
            headers={'X-API-Key': api_key},
            content_type='application/json'
        )
        
        assert response.status_code == 201
    
    def test_create_message_without_api_key(self, client):
        """Verifica que se pueda crear mensaje sin API Key (opcional)."""
        response = client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'msg-no-auth',
                'session_id': 'session-123',
                'content': 'Test message',
                'timestamp': '2025-12-04T15:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
