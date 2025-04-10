from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from jwt import ExpiredSignatureError
from models import db, RevokedToken
import os
from task_views import task_bp
from user_views import user_bp, init_db
from werkzeug.exceptions import HTTPException

def create_app(config_name="default"):
    """Creates and returns a new instance of Flask app."""
    load_dotenv()
    app = Flask(__name__)

    # Database settings
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Database in memory
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT settings
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "changeme")

    # Blueprints registration
    app.register_blueprint(user_bp)
    app.register_blueprint(task_bp)

    # Database and JWT initialization
    db.init_app(app)
    jwt = JWTManager(app)

    # Function to check if JWT token is revoked
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        token = db.session.get(RevokedToken, jwt_payload["jti"])
        return token is not None

    # Global error handler
    @app.errorhandler(Exception)
    def global_error_handler(error):
        if isinstance(error, HTTPException):
            response = jsonify({"error": error.description})
            response.status_code = error.code
        elif isinstance(error, ExpiredSignatureError):
            response = jsonify({"error": "Token has expired"})
            response.status_code = 401
        else:  # All other errors
            response = jsonify({"error": str(error)})
            response.status_code = 500
        return response

    # Fill database by initial values (only if we are not testing)
    with app.app_context():
        db.create_all()
        if config_name != "testing":
            init_db()
    return app


# Server start only if we run app directly
if __name__ == "__main__":
    app = create_app()
    port = os.getenv("TODOLIST_PORT", "80")
    app.run(host="0.0.0.0", port=port)
