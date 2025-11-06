from flask import Blueprint

def register_blueprints(app):
    from api.users import bp as users_bp
    from api.posts import bp as posts_bp
    
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
