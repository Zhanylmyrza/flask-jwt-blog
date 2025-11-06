from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from celery import Celery
from sqlalchemy.orm import sessionmaker


db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
celery = Celery()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        
        db.session_maker = sessionmaker(bind=db.engine)

def init_celery(app=None):
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery