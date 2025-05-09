from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, \
verify_jwt_in_request, get_jwt_identity, unset_jwt_cookies, get_jwt
from models import User, db, RevokedToken
import os
from werkzeug.security import check_password_hash, generate_password_hash

user_bp = Blueprint('user_bp', __name__)

# ============================================================
# 🚀 1. API ENDPOINTS (ROUTES)
# ============================================================

@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    admin_required(get_jwt_identity()) # only admin can get all users details
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    validate_access(user_id) # check if user tries to read other user account details
    user = db.session.get(User, user_id)
    if user is None:
        abort(404, "User not found.")
    return jsonify(user.to_dict())


@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user_role = data['role']
    if new_user_role == "Administrator":
        verify_jwt_in_request()
        admin_required(get_jwt_identity(), message="Access denied. Only administrators can create admin accounts.")
    hashed_password = generate_password_hash(data['password'])
    user = User(username=data['username'], email=data['email'], password=hashed_password, role=new_user_role)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@user_bp.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def edit_user(user_id):
    validate_access(user_id) # check if user tries to edit other user account
    request_data = request.get_json()
    if request_data.get('role') == 'Administrator':
        admin_required(get_jwt_identity())

    request_fields = set(request_data.keys())
    editable_fields = User.get_editable_fields()
    
    # PUT requires all values
    if request.method == 'PUT':
        if request_fields != editable_fields:
            abort(400, "Invalid request data structure.")

    user_to_update = db.session.get(User, user_id)
    if user_to_update is None:
        abort(404, "User not found.")
    for field_name in editable_fields:
        requested_value = request_data.get(field_name)
        if requested_value is None:
            continue
        new_value = generate_password_hash(requested_value) \
            if field_name == 'password' else requested_value
        setattr(user_to_update, field_name, new_value)
    db.session.commit()
    return jsonify(user_to_update.to_dict())


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def remove_user(user_id):
    validate_access(user_id) # Only admin can remove other users accounts
    user_to_delete = db.session.get(User, user_id)
    if user_to_delete is None:
        abort(404, "User not found.")
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({"msg": "User removed successfully."})


@user_bp.route('/login', methods=['POST'])
def user_login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    user_from_db=User.query.filter(User.username == username).first()
    if user_from_db is not None:
        password_hash = user_from_db.password
    else:
        abort(401, "User failed login")
    
    if password_hash and check_password_hash(password_hash, password):
        access_token = create_access_token(identity=str(user_from_db.id))
        response = jsonify({"msg": "User logged in successfully.", "user_id": user_from_db.id})
        set_access_cookies(response, access_token)
        return response
    else:
        abort(401, "User failed login")


@user_bp.route('/logout', methods=['GET'])
@jwt_required()
def user_logout():
    jti = get_jwt()["jti"]
    revoked_token = RevokedToken(jti=jti)
    db.session.add(revoked_token)
    db.session.commit()
    response = jsonify({"msg": "User logged out successfully."})
    unset_jwt_cookies(response)
    return response


# ============================================================
# 🔧 2. UTILITIES
# ============================================================

def admin_required(user_id, message='Access denied.'):
    user = db.session.get(User, user_id)
    if user is None or user.role != "Administrator":
        abort(403, message)


def validate_access(owner_id, message='Access denied.'):
    # Check if user try to access or edit resource that does not belong to them 
    logged_user_id = int(get_jwt_identity())
    logged_user_role = db.session.get(User, logged_user_id).role
    if logged_user_role != "Administrator" and logged_user_id != owner_id:
        abort(403, message)


def init_db():
    """Create default admin account if database is empty"""
    with db.session.begin():
        if not User.query.first():  # Check if user table is empty
            admin_username = os.getenv("TODOLIST_ADMIN_USERNAME", "admin")
            admin_email = os.getenv("TODOLIST_ADMIN_EMAIL", "admin@example.pl")
            admin_password = os.getenv("TODOLIST_ADMIN_PASSWORD", "admin")
            hashed_password = generate_password_hash(admin_password)
            admin = User(username=admin_username, email=admin_email, password=hashed_password, role='Administrator')
            db.session.add(admin)
            db.session.commit()
