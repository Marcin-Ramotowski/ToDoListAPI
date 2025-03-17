from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db
import os
from task_views import task_bp
from user_views import user_bp, init_db

if __name__ == "__main__":
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'changeme')
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)
    db.init_app(app)
    jwt = JWTManager(app)
    with app.app_context():
        db.create_all()
        init_db()
    app.run(host='0.0.0.0')
