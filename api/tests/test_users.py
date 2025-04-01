from conftest import login_test_user
import json

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
    headers = login_test_user(test_user.id)
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json", headers=headers)
    assert response.status_code == 403 # Common user cannot create admin users

    # Try to create admin user using admin account
    headers = login_test_user(test_admin.id)
    response = test_client.post("/users", data=json.dumps(admin_user_data), content_type="application/json", headers=headers)
    assert response.status_code == 201 # Logged administrators can create new admin users

def test_edit_user(test_client, test_user, test_admin):
    "User edit test"
    # Anonymous cannot edit any user
    admin_data = test_admin.to_dict()
    response = test_client.patch(f"/users/{test_admin.id}", data=json.dumps({"username": admin_data["username"], "password": "adminpass"}))
    assert response.status_code == 401

    # Login users (get dict with auth header and merge it with dict with rest of headers)
    admin_headers = login_test_user(test_admin.id) | {"Content-Type": "application/json"}
    user_headers = login_test_user(test_user.id) | {"Content-Type": "application/json"}

    # Check if PUT request contains all editable fields
    response = test_client.put(f"/users/{test_user.id}", data=json.dumps({"username": test_user.username, "password": "testpass"}), headers=user_headers)
    assert response.status_code == 400 # PUT must have all editable fields

    # Check if user can edit their own data
    response = test_client.patch(f"/users/{test_user.id}", data=json.dumps({"username": test_user.username, "password": "testpass"}), headers=user_headers)
    assert response.status_code == 200

    # Check if user cannot edit other user data
    response = test_client.patch(f"/users/{test_admin.id}", data=json.dumps({"username": admin_data["username"], "password": "adminpass"}), headers=user_headers)
    assert response.status_code == 403

    # Check if admin can edit other user data
    response = test_client.patch(f"/users/{test_user.id}", data=json.dumps({"username": test_user.username, "password": "testpass"}), headers=admin_headers)
    assert response.status_code == 200

def test_remove_user(test_client, test_user, test_user2, test_admin):
    "User remove test"
    # Anonymous try to remove user
    response = test_client.delete(f"/users/{test_user.id}")
    assert response.status_code == 401 # Anonymous cannot remove user account

    # Logged user try to remove other user account
    headers = login_test_user(test_user.id)
    response = test_client.delete(f"/users/{test_admin.id}", headers=headers)
    assert response.status_code == 403 # Common user cannot remove other user account

    # Logged user try to remove own account
    response = test_client.delete(f"/users/{test_user.id}", headers=headers)
    assert response.status_code == 200 # Common user can remove their own account

    # Logged admin can remove other user account
    admin_headers = login_test_user(test_admin.id)
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

def test_get_users(test_client, test_user, test_admin):
    """Get all users test"""
    response = test_client.get("/users")
    assert response.status_code == 401 # Anonymous cannot get all users data
    
    # Common user try to get all users data
    headers = login_test_user(test_user.id)
    response = test_client.get("/users", headers=headers)
    assert response.status_code == 403 # Common user cannot get all users data
    
    # Admin user try to get all users data
    headers = login_test_user(test_admin.id)
    response = test_client.get("/users", headers=headers)
    assert response.status_code == 200 # Admin user should be able to get all users data

def test_get_user_with_token(test_client, test_user, test_admin):
    """Test to get user data before and after auth using JWT token"""
    response = test_client.get(f"/users/{test_admin.id}")
    assert response.status_code == 401 # Try to get user data without login

    admin_headers = login_test_user(test_admin.id)
    response = test_client.get(f"/users/{test_admin.id}", headers=admin_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data["username"] == "adminuser"

    headers = login_test_user(test_user.id)
    response = test_client.get(f"/users/{test_user.id}", headers=headers)
    assert response.status_code == 200 # Common user can get own user data
    response = test_client.get(f"/users/{test_admin.id}", headers=headers)
    assert response.status_code == 403 # Common user cannot get other user data
    response = test_client.get(f"/users/{test_user.id}", headers=admin_headers)
    assert response.status_code == 200 # Admin can access all user data

def test_user_logout(test_client, test_user):
    """Test if logout works and JWT token is revoked"""
    headers = login_test_user(test_user.id)
    response = test_client.get(f"/logout", headers=headers)
    assert response.status_code == 200 # Logged user can logout
    response = test_client.get(f"/logout", headers=headers)
    assert response.status_code == 401 # Token should be revoked after logout
