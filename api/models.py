from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum('Administrator', 'User'), default='User')
    password = db.Column(db.String(162), nullable=False)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email, "role": self.role}
    
    @classmethod
    def get_editable_fields():
        return {"username", "email", "role", "password"}

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "done": self.done,
        }
    
    @classmethod
    def get_editable_fields():
        return {"title", "description", "due_date", "done"}
