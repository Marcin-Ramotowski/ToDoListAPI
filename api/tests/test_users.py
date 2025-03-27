import json
from models import User, db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

def test_create_user(test_client):
    """New user registration test"""

    # Anonymous try to create common user
    test_user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass", "role": "User"}
    response = test_client.post("/users", data=json.dumps(test_user_data), content_type="application/json")
    assert response.status_code == 201 # User should be created successfully
    data = response.get_json()
    assert data["username"] == "testuser"

    # Anonymous try to create admin user
    admin_user_data = {"username": "testadmin", "email": "testadmin@example.com", "password": "adminpass", "role": "Administrator"}
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json")
    assert response.status_code == 401 # Anonymous cannot create admin users

    # Login common user and try to create admin user
    access_token = create_access_token(identity='1')
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json", headers=headers)
    assert response.status_code == 403 # Common user cannot create admin users

    # Try to create admin user using admin account
    hashed_pass = generate_password_hash("adminpass")
    user = User(username="admin", email="admin@example.com", password=hashed_pass, role="Administrator")
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json", headers=headers)
    assert response.status_code == 201 # Logged administrators can create new admin users


def test_login(test_client):
    """User login test"""
    hashed_pass = generate_password_hash("testpass")
    user = User(username="testuser", email="test@example.com", password=hashed_pass, role="User")
    db.session.add(user)
    db.session.commit()

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
    assert response.status_code == 200 # Admin user should can get all users data

def test_get_user_with_token(test_client):
    """Test to get user data before and after auth using JWT token"""
    admin_pass = generate_password_hash("admin_pass")
    admin = User(username="admin", email="admin@example.com", password=admin_pass, role="Administrator")
    db.session.add(admin)
    db.session.commit()

    response = test_client.get(f"/users/{admin.id}")
    assert response.status_code == 401 # Try to get user data without login
    
    access_token = create_access_token(identity=str(admin.id))
    admin_headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.get(f"/users/{admin.id}", headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "admin"

    user_pass = generate_password_hash("test_pass")
    user = User(username="testuser", email="test@example.com", password=user_pass, role="User")
    db.session.add(user)
    db.session.commit()
    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}
    response = test_client.get(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200 # Common user can get own user data
    response = test_client.get(f"/users/{admin.id}", headers=headers)
    assert response.status_code == 403 # Common user cannot get other user data
    response = test_client.get(f"/users/{user.id}", headers=admin_headers)
    assert response.status_code == 200 # Admin can access all user data
