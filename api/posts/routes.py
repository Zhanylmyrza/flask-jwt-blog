from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import bp
from .models import Post
from .schemas import post_schema, posts_schema
from extensions import db



@bp.route('/', methods=['POST'], strict_slashes=False)
@jwt_required()
def create_post():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    if not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Title and content required'}), 400

    data['user_id'] = int(get_jwt_identity())
    post = Post(**data)
    db.session.add(post)
    db.session.commit()
    return jsonify(post_schema.dump(post)), 201



@bp.route('/', methods=['GET'], strict_slashes=False)
def get_posts():
    posts = Post.query.all()
    return jsonify(posts_schema.dump(posts)), 200

@bp.route('/<int:id>', methods=['GET'], strict_slashes=False)
def get_post(id):
    post = db.session.get(Post, id)
    if post is None:
        abort(404)
    return jsonify(post_schema.dump(post)), 200

@bp.route('/<int:id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_post(id):
    post = db.session.get(Post, id)
    if post is None:
        abort(404)
    if int(get_jwt_identity()) != post.user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    data = request.get_json()
    for key, value in data.items():
        setattr(post, key, value)
    
    db.session.commit()
    return jsonify(post_schema.dump(post)), 200

@bp.route('/<int:id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_post(id):
    post = db.session.get(Post, id)
    if post is None:
        abort(404)
    if int(get_jwt_identity()) != post.user_id:
        return jsonify({'message': 'Unauthorized'}), 403
    
    db.session.delete(post)
    db.session.commit()
    return '', 204

