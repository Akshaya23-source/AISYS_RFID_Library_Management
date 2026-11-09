from flask import Flask
from app.db import init_db

def create_app():
    app = Flask(__name__)

    # Initialize database
    init_db()

    # Register routes
    from app.routes import bp
    app.register_blueprint(bp)

    return app