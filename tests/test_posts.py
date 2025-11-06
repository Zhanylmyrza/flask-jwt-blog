import pytest
from api.posts.models import Post

def test_create_post_unauthorized(client):
    
    response = client.post('/api/posts', json={
        'title': 'Test Post',
        'content': 'Test Content'
    })
    assert response.status_code == 401

def test_create_post_authorized(client, test_user, session):
    
    # First login to get token
    login_response = client.post('/api/users/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    # Create post with token
    response = client.post('/api/posts', json={
        'title': 'Test Post',
        'content': 'Test Content'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 201
    assert response.json['title'] == 'Test Post'
    assert response.json['content'] == 'Test Content'
    assert 'created_at' in response.json

def test_get_posts(client):
    
    response = client.get('/api/posts')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_post_detail(client, test_user, session):
    
    
    post = Post(title='Test Post', content='Test Content', user_id=test_user.id)
    session.add(post)
    session.commit()
    
    
    response = client.get(f'/api/posts/{post.id}')
    assert response.status_code == 200
    assert response.json['title'] == 'Test Post'
    assert response.json['content'] == 'Test Content'

def test_update_post_unauthorized(client, test_user, session):
    
    post = Post(title='Test Post', content='Test Content', user_id=test_user.id)
    session.add(post)
    session.commit()
    
    response = client.put(f'/api/posts/{post.id}', json={
        'title': 'Updated Title',
        'content': 'Updated Content'
    })
    assert response.status_code == 401

def test_update_post_authorized(client, test_user, session):
    
    
    post = Post(title='Test Post', content='Test Content', user_id=test_user.id)
    session.add(post)
    session.commit()
    
    
    login_response = client.post('/api/users/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    
    response = client.put(f'/api/posts/{post.id}', json={
        'title': 'Updated Title',
        'content': 'Updated Content'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Title'
    assert response.json['content'] == 'Updated Content'

def test_delete_post_unauthorized(client, test_user, session):
    
    post = Post(title='Test Post', content='Test Content', user_id=test_user.id)
    session.add(post)
    session.commit()
    
    response = client.delete(f'/api/posts/{post.id}')
    assert response.status_code == 401

def test_delete_post_authorized(client, test_user, session):
    
    post = Post(title='Test Post', content='Test Content', user_id=test_user.id)
    session.add(post)
    session.commit()
    
    
    login_response = client.post('/api/users/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    
    response = client.delete(f'/api/posts/{post.id}', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 204
    
    
    response = client.get(f'/api/posts/{post.id}')
    assert response.status_code == 404