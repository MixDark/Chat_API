"""
Tests para funcionalidad de búsqueda de mensajes.
"""
import json


class TestSearchEndpoints:
    """Tests para endpoint de búsqueda."""
    
    def setup_method(self):
        """Crea mensajes de prueba antes de cada test."""
        pass
    
    def test_search_by_content(self, client):
        """Verifica búsqueda por contenido."""
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-1',
                'session_id': 'search-session',
                'content': 'Necesito ayuda con mi cuenta',
                'timestamp': '2025-12-04T10:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-2',
                'session_id': 'search-session',
                'content': 'Información sobre productos',
                'timestamp': '2025-12-04T11:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/messages/search-session/search?q=ayuda')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'success'
        assert len(data['data']) == 1
        assert 'ayuda' in data['data'][0]['content']
    
    def test_search_by_sender(self, client):
        """Verifica búsqueda por remitente."""
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-3',
                'session_id': 'search-session-2',
                'content': 'Mensaje del sistema',
                'timestamp': '2025-12-04T10:00:00Z',
                'sender': 'system'
            }),
            content_type='application/json'
        )
        
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-4',
                'session_id': 'search-session-2',
                'content': 'Mensaje del usuario',
                'timestamp': '2025-12-04T11:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/messages/search-session-2/search?sender=user')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) == 1
        assert data['data'][0]['sender'] == 'user'
    
    def test_search_by_date_range(self, client):
        """Verifica búsqueda por rango de fechas."""
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-5',
                'session_id': 'search-session-3',
                'content': 'Mensaje antiguo',
                'timestamp': '2025-12-01T10:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-6',
                'session_id': 'search-session-3',
                'content': 'Mensaje reciente',
                'timestamp': '2025-12-04T10:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        response = client.get(
            '/api/messages/search-session-3/search?start_date=2025-12-04T00:00:00Z&end_date=2025-12-04T23:59:59Z'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) == 1
        assert 'reciente' in data['data'][0]['content']
    
    def test_search_combined_filters(self, client):
        """Verifica búsqueda con múltiples filtros."""
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-7',
                'session_id': 'search-session-4',
                'content': 'Usuario necesita ayuda',
                'timestamp': '2025-12-04T10:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-8',
                'session_id': 'search-session-4',
                'content': 'Sistema proporciona ayuda',
                'timestamp': '2025-12-04T11:00:00Z',
                'sender': 'system'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/messages/search-session-4/search?q=ayuda&sender=user')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) == 1
        assert data['data'][0]['sender'] == 'user'
        assert 'ayuda' in data['data'][0]['content']
    
    def test_search_with_pagination(self, client):
        """Verifica paginación en búsqueda."""
        for i in range(15):
            client.post(
                '/api/messages',
                data=json.dumps({
                    'message_id': f'search-page-{i}',
                    'session_id': 'search-session-5',
                    'content': f'Mensaje de prueba {i}',
                    'timestamp': '2025-12-04T10:00:00Z',
                    'sender': 'user'
                }),
                content_type='application/json'
            )
        
        response = client.get('/api/messages/search-session-5/search?q=prueba&limit=5&offset=0')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) == 5
        assert data['pagination']['total'] == 15
        assert data['pagination']['limit'] == 5
        assert data['pagination']['offset'] == 0
    
    def test_search_no_results(self, client):
        """Verifica búsqueda sin resultados."""
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-9',
                'session_id': 'search-session-6',
                'content': 'Mensaje de prueba',
                'timestamp': '2025-12-04T10:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/messages/search-session-6/search?q=inexistente')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) == 0
        assert data['pagination']['total'] == 0
    
    def test_search_empty_query(self, client):
        """Verifica búsqueda con query vacío retorna todos."""
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-10',
                'session_id': 'search-session-7',
                'content': 'Mensaje 1',
                'timestamp': '2025-12-04T10:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        client.post(
            '/api/messages',
            data=json.dumps({
                'message_id': 'search-11',
                'session_id': 'search-session-7',
                'content': 'Mensaje 2',
                'timestamp': '2025-12-04T11:00:00Z',
                'sender': 'user'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/messages/search-session-7/search?q=')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data['data']) >= 2
