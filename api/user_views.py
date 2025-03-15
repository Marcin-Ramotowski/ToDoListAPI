from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies
from models import User, db
from werkzeug.security import check_password_hash, generate_password_hash

user_bp = Blueprint('user_bp', __name__)

def admin_required():
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    if not current_user or current_user.role != 'admin':
        abort(403, {'error': 'Access denied.'})

@user_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required()
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
@admin_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
    current_user = User.query.filter_by(username=get_jwt_identity()).first()
    request_data = request.get_json()
    user_to_update = User.query.get_or_404(user_id)
    request_username = request_data.get('username')
    request_email = request_data.get('email')
    if request_username and request_email:
        user_to_update.username = request_username
        user_to_update.email = request_email
        db.session.commit()
        return jsonify(user_to_update.to_dict())
    else:
        return abort(400, {'error': 'Incomplete user data.'})

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({})

@user_bp.route('/login', methods=['POST'])
def user_login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    password_hash = generate_password_hash(password)

    user_from_db=User.query.filter(User.username == username).first()
    if user_from_db is not None:
        password_from_db = user_from_db.password
    else:
        return jsonify({"msg": f"User {username} failed login"})
    
    if password_from_db and check_password_hash(password_hash, password_from_db):
        access_token = create_access_token(identity=username)
        response = jsonify({"msg": f"User {username} logged in successfully."})
        set_access_cookies(response, access_token)
        return response
    else:
        return jsonify({"msg": f"User {username} failed login."})

@user_bp.route('/logout', methods=['GET'])
@jwt_required()
def user_logout():
    current_user = get_jwt_identity()
    response = jsonify({"msg": f"User {current_user} logged out successfully."})
    unset_jwt_cookies(response)
    return response