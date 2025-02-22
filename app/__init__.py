from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from app.config import Config

# Initialize addon instances
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Within the app context
    with app.app_context():

        # Import model classes for migration
        from app.models.Supermarket.model import Supermarket
        from app.models.Branch.model import Branch
        from app.models.DatasetFile.model import DatasetFile
        from app.models.Optimization.model import Optimization
        from app.models.Prediction.model import Prediction
        from app.models.Segmentation.model import Segmentation
        from app.models.Cluster.model import Cluster

        # Setup admin views

        # Import routes
        from app.blueprints.main import routes
        from app.blueprints.auth import routes
        from app.blueprints.prediction import routes
        from app.blueprints.segmentation import routes

        # Register blueprints
        from app.blueprints.main import main_bp
        from app.blueprints.auth import auth_bp
        from app.blueprints.prediction import prediction_bp
        from app.blueprints.segmentation import segmentation_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(prediction_bp)
        app.register_blueprint(segmentation_bp)

    return app
