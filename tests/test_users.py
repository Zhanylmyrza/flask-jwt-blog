def test_register(client, session):
    
    with client:
        response = client.post('/api/users/register', json={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        })
        assert response.status_code == 201
        assert 'username' in response.json
        assert response.json['username'] == 'newuser'

def test_login(client, test_user, session):
    
    with client:
        response = client.post('/api/users/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert 'access_token' in response.json

def test_get_users_unauthorized(client):
    
    with client:
        response = client.get('/api/users/')
        assert response.status_code == 401

def test_get_users_authorized(client, test_user, session):
    
    with client:
        
        login_response = client.post('/api/users/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        assert login_response.status_code == 200
        token = login_response.json['access_token']
        
        
        response = client.get('/api/users/', headers={
            'Authorization': f'Bearer {token}'
        })
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) > 0