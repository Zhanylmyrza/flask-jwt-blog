from flask import jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.http import HTTP_STATUS_CODES

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        """Handle HTTP errors."""
        response = {
            'error': HTTP_STATUS_CODES.get(error.code, 'Unknown error'),
            'message': error.description,
            'status_code': error.code
        }
        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle non-HTTP errors."""
        response = {
            'error': 'Internal Server Error',
            'message': str(error),
            'status_code': 500
        }
        return jsonify(response), 500

    
    @app.errorhandler(422)
    def handle_validation_error(error):
        """Handle validation errors."""
        response = {
            'error': 'Validation Error',
            'message': error.description,
            'errors': error.exc.messages if hasattr(error, 'exc') else None,
            'status_code': 422
        }
        return jsonify(response), 422

    @app.errorhandler(401)
    def handle_unauthorized_error(error):
        """Handle unauthorized access errors."""
        response = {
            'error': 'Unauthorized',
            'message': 'The server could not verify your authentication credentials.',
            'status_code': 401
        }
        return jsonify(response), 401

    @app.errorhandler(403)
    def handle_forbidden_error(error):
        """Handle forbidden access errors."""
        response = {
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource.',
            'status_code': 403
        }
        return jsonify(response), 403

    @app.errorhandler(404)
    def handle_not_found_error(error):
        """Handle resource not found errors."""
        response = {
            'error': 'Not Found',
            'message': 'The requested resource was not found on the server.',
            'status_code': 404
        }
        return jsonify(response), 404