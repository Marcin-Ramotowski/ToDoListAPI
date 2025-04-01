import json
from models import User, db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

def test_create_user(test_client, test_user, test_admin):
    """New user registration test"""

    # Anonymous try to create common user
    test_user_data = {"username": "test", "email": "testemail@example.com", "password": "testpassword", "role": "User"}
    response = test_client.post("/users", data=json.dumps(test_user_data), content_type="application/json")
    assert response.status_code == 201 # User should be created successfully
    data = response.get_json()
    assert data["username"] == "test"

    # Anonymous try to create admin user
    admin_user_data = {"username": "testadmin", "email": "testadmin@example.com", "password": "adminpass", "role": "Administrator"}
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json")
    assert response.status_code == 401 # Anonymous cannot create admin users

    # Login common user and try to create admin user
    access_token = create_access_token(identity=str(test_user.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json", headers=headers)
    assert response.status_code == 403 # Common user cannot create admin users

    # Try to create admin user using admin account
    access_token = create_access_token(identity=str(test_admin.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json", headers=headers)
    assert response.status_code == 201 # Logged administrators can create new admin users

def test_edit_user(test_client, test_user):
    "User edit test"
    # Create one admin account
    admin_password = "adminpass"
    hashed_admin_pass = generate_password_hash(admin_password)
    admin_data = {"username": "testadmin", "email": "testadmin@example.com", "role": "Administrator"}
    admin = User(username=admin_data["username"], email=admin_data["email"], password=hashed_admin_pass, role=admin_data["role"])
    db.session.add(admin)
    db.session.commit()

    # Anonymous cannot edit any user
    response = test_client.patch(f"/users/{admin.id}", data=json.dumps({"username": admin_data["username"], "password": admin_password}))
    assert response.status_code == 401

    # Login users
    admin_access_token = create_access_token(identity=str(admin.id))
    admin_headers = {"Authorization": f"Bearer {admin_access_token}", "Content-Type": "application/json"}
    user_access_token = create_access_token(identity=str(test_user.id))
    user_headers = {"Authorization": f"Bearer {user_access_token}", "Content-Type": "application/json"}

    # Check if PUT request contains all editable fields
    response = test_client.put(f"/users/{test_user.id}", data=json.dumps({"username": test_user.username, "password": "testpass"}), headers=user_headers)
    assert response.status_code == 400 # PUT must have all editable fields

    # Check if user can edit their own data
    response = test_client.patch(f"/users/{test_user.id}", data=json.dumps({"username": test_user.username, "password": "testpass"}), headers=user_headers)
    assert response.status_code == 200

    # Check if user cannot edit other user data
    response = test_client.patch(f"/users/{admin.id}", data=json.dumps({"username": admin_data["username"], "password": admin_password}), headers=user_headers)
    assert response.status_code == 403

    # Check if admin can edit other user data
    response = test_client.patch(f"/users/{test_user.id}", data=json.dumps({"username": test_user.username, "password": "testpass"}), headers=admin_headers)
    assert response.status_code == 200

def test_remove_user(test_client, test_user, test_user2):
    "User remove test"
    # Create 1 admin account
    hashed_pass = generate_password_hash("adminpass")
    admin = User(username="testadmin", email="testadmin@example.com", password=hashed_pass, role="Administrator")
    db.session.add(admin)
    db.session.commit()

    # Anonymous try to remove user
    response = test_client.delete(f"/users/{test_user.id}")
    assert response.status_code == 401 # Anonymous cannot remove user account

    # Logged user try to remove other user account
    access_token = create_access_token(identity=str(test_user.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.delete(f"/users/{admin.id}", headers=headers)
    assert response.status_code == 403 # Common user cannot remove other user account

    # Logged user try to remove own account
    response = test_client.delete(f"/users/{test_user.id}", headers=headers)
    assert response.status_code == 200 # Common user can remove their own account

    # Logged admin can remove other user account
    admin_access_token = create_access_token(identity=str(admin.id))
    admin_headers = {"Authorization": f"Bearer {admin_access_token}"}
    response = test_client.delete(f"/users/{test_user2.id}", headers=admin_headers)
    assert response.status_code == 200 # Admin user can remove other user account

def test_login(test_client, test_user):
    """User login test"""

    response = test_client.post(
        "/login",
        data=json.dumps({"username": "testuser", "password": "wrongpass"}),
        content_type="application/json",
    )
    assert response.status_code == 401 # User should not be logged - wrong password
    response = test_client.post(
        "/login",
        data=json.dumps({"username": "testuser", "password": "testpass"}),
        content_type="application/json",
    )
    assert response.status_code == 200 # User should be logged - right password

def test_get_users(test_client):
    """Get all users test"""
    response = test_client.get("/users")
    assert response.status_code == 401 # Anonymous cannot get all users data
    
    # Common user try to get all users data
    hashed_pass = generate_password_hash("testpass")
    user = User(username="testuser", email="test@example.com", password=hashed_pass, role="User")
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/users", headers=headers)
    assert response.status_code == 403 # Common user cannot get all users data
    
    # Admin user try to get all users data
    hashed_pass = generate_password_hash("adminpass")
    user = User(username="testadmin", email="testadmin@example.com", password=hashed_pass, role="Administrator")
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get("/users", headers=headers)
    assert response.status_code == 200 # Admin user should be able to get all users data

def test_get_user_with_token(test_client, test_user, test_admin):
    """Test to get user data before and after auth using JWT token"""
    response = test_client.get(f"/users/{test_admin.id}")
    assert response.status_code == 401 # Try to get user data without login
    
    access_token = create_access_token(identity=str(test_admin.id))
    admin_headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.get(f"/users/{test_admin.id}", headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "adminuser"

    access_token = create_access_token(identity=str(test_user.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get(f"/users/{test_user.id}", headers=headers)
    assert response.status_code == 200 # Common user can get own user data
    response = test_client.get(f"/users/{test_admin.id}", headers=headers)
    assert response.status_code == 403 # Common user cannot get other user data
    response = test_client.get(f"/users/{test_user.id}", headers=admin_headers)
    assert response.status_code == 200 # Admin can access all user data

def test_user_logout(test_client, test_user):
    """Test if logout works and JWT token is revoked"""
    access_token = create_access_token(identity=str(test_user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.get(f"/logout", headers=headers)
    assert response.status_code == 200 # Logged user can logout
    response = test_client.get(f"/logout", headers=headers)
    assert response.status_code == 401 # Token should be revoked after logout
