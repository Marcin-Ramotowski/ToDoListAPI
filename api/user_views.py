from flask import Blueprint, jsonify, request, abort, g
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, unset_jwt_cookies
from models import User, db
from werkzeug.security import check_password_hash, generate_password_hash

user_bp = Blueprint('user_bp', __name__)

def admin_required(user_id):
    user = User.query.get(user_id)
    if user is None or user.role != "Administrator":
        return jsonify({'error': f'Access denied.'}), 403

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    admin_required(get_jwt_identity())
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    logged_user_id = int(get_jwt_identity())
    logged_user_role = User.query.get(logged_user_id).role
    if logged_user_role != "Administrator" and logged_user_id != user_id:
        return jsonify({'error': f'Access denied.'}), 403
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user_role = data['role']
    # Only administrator can create admin accounts
    if new_user_role == "Administrator":
        logged_user_id = int(get_jwt_identity())
        logged_user_role = User.query.get(logged_user_id).role
        if logged_user_role != "Administrator":
            return jsonify({'error': f'You can not create admin users.'}), 403
    user = User(username=data['username'], email=data['email'], password=data['password'], role=new_user_role)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def edit_user(user_id):
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
        return jsonify({"msg": "User failed login"})
    
    if password_from_db and check_password_hash(password_hash, password_from_db):
        access_token = create_access_token(identity=str(user_from_db.id))
        response = jsonify({"msg": "User logged in successfully."})
        set_access_cookies(response, access_token)
        return response
    else:
        return jsonify({"msg": "User failed login."})

@user_bp.route('/logout', methods=['GET'])
@jwt_required()
def user_logout():
    response = jsonify({"msg": "User logged out successfully."})
    unset_jwt_cookies(response)
    return response