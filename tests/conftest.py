import os
import sys
import pytest
from app import create_app
from extensions import db
from api.users.models import User

@pytest.fixture
def app():
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    return app

@pytest.fixture
def client(app):
    
    return app.test_client()

@pytest.fixture
def _db(app):
    
    with app.app_context():
        db.create_all()
        
        
        from sqlalchemy.orm import sessionmaker
        db.session_maker = sessionmaker(bind=db.engine)
        
        yield db
        db.drop_all()

@pytest.fixture
def session(app, _db):
    
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()
        
        session = _db.session_maker()
        
        yield session
        
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def test_user(session):
    
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    session.add(user)
    session.commit()
    return user