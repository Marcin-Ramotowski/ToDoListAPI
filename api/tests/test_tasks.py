from datetime import datetime
import json
from models import Task, User, db
from flask_jwt_extended import create_access_token

def test_create_task(test_client):
    """Task creation test by logged in user"""
    user = User(username="testuser", email="test@example.com", password="hashed_pass", role="User")
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.post(
        "/tasks",
        data=json.dumps({"title": "Test Task", "description": "Opis", "due_date": "20-03-2025 12:00", "done": 0}),
        headers=headers,
        content_type="application/json",
    )
    assert response.status_code == 200  # Create task should be successful
    data = response.get_json()
    assert data["title"] == "Test Task"

def test_get_tasks(test_client):
    """User task get test"""
    user = User(username="taskuser", email="task@example.com", password="hashed_pass", role="User")
    db.session.add(user)
    db.session.commit()

    task = Task(title="Zadanie", description="Opis zadania", due_date=datetime.strptime("20-03-2025 12:00", '%d-%m-%Y %H:%M'), done=0, user_id=user.id)
    db.session.add(task)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    headers = {"Authorization": f"Bearer {access_token}"}

    response = test_client.get(f"/tasks/user/{user.id}", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["title"] == "Zadanie"
