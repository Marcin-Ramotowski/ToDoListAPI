import json
from models import User, db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

def test_create_user(test_client):
    """New user registration test"""
    response = test_client.post(
        "/users",
        data=json.dumps({"username": "testuser", "email": "test@example.com", "password": "testpass", "role": "User"}),
        content_type="application/json",
    )
    assert response.status_code == 201 # User should be created successfully
    data = response.get_json()
    assert data["username"] == "testuser"

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
    """Get all users test - JWT required"""
    response = test_client.get("/users")
    assert response.status_code == 401

def test_get_user_with_token(test_client):
    """Test to get user data after auth using JWT token"""
    user = User(username="admin", email="admin@example.com", password="hashed_pass", role="Administrator")
    print(user.id)
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.get(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "admin"
