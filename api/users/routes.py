from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from . import bp
from .models import User
from .schemas import user_schema, users_schema
from extensions import db
from marshmallow import ValidationError


@bp.route('/register', methods=['POST'])
def register():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'message': 'Validation error', 'errors': err.messages}), 422

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400

    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify(user_schema.dump(user)), 201



@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity= str(user.id))
    return jsonify({'access_token': access_token}), 200



@bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200



@bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = db.session.get(User, id)
    if user is None:
        abort(404)
    return jsonify(user_schema.dump(user)), 200



@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = db.session.get(User, id)
    if user is None:
        abort(404)
    current_user_id = int(get_jwt_identity()) 
    if current_user_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if 'username' in data:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        user.username = data['username']

    if 'email' in data:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        user.email = data['email']

    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user_schema.dump(user)), 200



@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = db.session.get(User, id)
    if user is None:
        abort(404)
    current_user_id = int(get_jwt_identity())
    if current_user_id != user.id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(user)
    db.session.commit()
    return '', 204

