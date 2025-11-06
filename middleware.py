from flask import request, g
from time import time
import logging

logger = logging.getLogger(__name__)

def register_middleware(app):
    
    @app.before_request
    def before_request():
        """Execute before each request."""
        
        g.start_time = time()
        
        
        logger.info(f'Incoming {request.method} request to {request.path}')
        
        # You could add rate limiting here
        # You could check API keys here
        # You could load user data here
    
    
    @app.after_request
    def after_request(response):
        """Execute after each request."""
        
        duration = time() - g.start_time
        
        
        response.headers['X-Request-Duration'] = str(duration)
        response.headers['X-API-Version'] = '1.0'
        
        
        logger.info(f'Request completed in {duration:.2f}s with status {response.status_code}')
        
        return response