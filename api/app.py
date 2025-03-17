from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from jwt import ExpiredSignatureError
from models import db
import os
from task_views import task_bp
from user_views import user_bp, init_db
from werkzeug.exceptions import HTTPException

# App initialization
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'changeme')

# Blueprints registration
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)

# Database and JWT initialization
db.init_app(app)
jwt = JWTManager(app)

# Global error handler
@app.errorhandler(Exception)
def global_error_handler(error):
    if isinstance(error, HTTPException):
        response = jsonify({"error": error.description})
        response.status_code = error.code
    elif isinstance(error, ExpiredSignatureError):
        response = jsonify({"error": "Token has expired"})
        response.status_code = 401
    else:  # Wszystkie inne błędy
        response = jsonify({"error": str(error)})
        response.status_code = 500
    return response


# Fill database by initial values
with app.app_context():
    db.create_all()
    init_db()

# Server start
if __name__ == "__main__":
    app.run(host='0.0.0.0')
