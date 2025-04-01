import pytest
from app import create_app
from datetime import datetime
from models import db, User, Task
from werkzeug.security import generate_password_hash

@pytest.fixture
def test_client():
    """Creates a new instance of test app."""
    app = create_app("testing")
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def test_user():
    """Create a new user for testing."""
    user = User(username="testuser", email="test@example.com", password=generate_password_hash("testpass"), role="User")
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_user2():
    """Create a user nr 2 for testing."""
    user2 = User(username="testuser2", email="test2@example.com", password=generate_password_hash("testpass2"), role="User")
    db.session.add(user2)
    db.session.commit()
    return user2

@pytest.fixture
def test_admin():
    """Create a new admin user for testing."""
    admin = User(username="adminuser", email="admin@example.com", password=generate_password_hash("adminpass"), role="Administrator")
    db.session.add(admin)
    db.session.commit()
    return admin

@pytest.fixture
def new_task(test_user):
    """Create a new task for testing."""
    due_date = datetime.strptime("20-03-2025 12:00", '%d-%m-%Y %H:%M')
    task = Task(title="Test Task", description="Task description", due_date=due_date, done=0, user_id=test_user.id)
    db.session.add(task)
    db.session.commit()
    return task
