import os
from flask import Flask
from config import Config
from database.models import db
from services.scheduler import init_scheduler
from routes.auth import auth_bp
from routes.capsule import capsule_bp
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Database
    db.init_app(app)

    # Logging
    logging.basicConfig(level=logging.INFO)
    app.logger.info("Application starting up...")

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(capsule_bp)

    with app.app_context():
        import database.models
        # Don't create all here in production normally. For this specific local project, it's fine.
        db.create_all()
        app.logger.info("Database tables verified.")
    
    # Initialize Scheduler
    init_scheduler(app)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False) # use_reloader=False to prevent double scheduler instances
