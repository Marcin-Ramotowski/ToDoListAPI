import json
from flask_jwt_extended import create_access_token

def test_create_task(test_client, test_user):
    """Task creation test by logged in user"""
    access_token = create_access_token(identity=str(test_user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.post(
        "/tasks",
        data=json.dumps({"title": "Test Task", "description": "Opis", "due_date": "20-03-2025 12:00", "done": 0}),
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 200, "Logged user should can create task"
    data = response.get_json()
    assert data["title"] == "Test Task", "API should return created task data"

def test_get_tasks(test_client, test_user, new_task):
    """User task get test"""
    access_token = create_access_token(identity=str(test_user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.get(f"/tasks/user/{test_user.id}", headers=headers)
    assert response.status_code == 200, "Logged user should can get your own tasks data"
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task", "API should return only tasks belongs to specific user"
