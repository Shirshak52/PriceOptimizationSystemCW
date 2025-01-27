from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

# Initialize addon instances
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():

        # Import model classes for migration
        from app.models.supermarket import Supermarket
        from app.models.branch import Branch
        from app.models.dataset_file import DatasetFile
        from app.models.optimization import Optimization
        from app.models.prediction import Prediction
        from app.models.segmentation import Segmentation
        from app.models.cluster import Cluster

        # Setup admin views

        # Import routes
        from app.blueprints.main.routes import index

        # Register blueprints
        from app.blueprints.main import main_bp

        app.register_blueprint(main_bp)

    return app
