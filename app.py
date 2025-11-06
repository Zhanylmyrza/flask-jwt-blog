
from flask import Flask
from flask_restful import Api
from config import Config
from extensions import db, jwt, mail, init_celery, init_db
from api import register_blueprints
from errors import register_error_handlers
from middleware import register_middleware
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    
    init_db(app)  
    jwt.init_app(app)
    mail.init_app(app)
    init_celery(app)

    
    register_error_handlers(app)
    register_middleware(app)
    register_blueprints(app)

    
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
