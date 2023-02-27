from flask import Flask
from models import db
from user_views import user_bp
from task_views import task_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)

db.init_app(app)

with app.app_context():
    db.create_all()
