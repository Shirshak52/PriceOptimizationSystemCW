from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_session import Session as FlaskSession
from app.config import Config

# Initialize addon instances
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
flask_session = FlaskSession()


def create_app(config_class=Config):
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    flask_session.init_app(app)

    # Within the app context
    with app.app_context():

        # Import model classes for migration
        from app.models.Supermarket.model import Supermarket
        from app.models.Branch.model import Branch
        from app.models.DatasetFile.model import DatasetFile
        from app.models.Optimization.model import Optimization
        from app.models.OptimizedPrices.model import OptimizedPrices
        from app.models.OptimizedSales.model import OptimizedSales
        from app.models.Prediction.model import Prediction
        from app.models.Segmentation.model import Segmentation
        from app.models.Cluster.model import Cluster

        # Setup admin views

        # Import routes
        from app.blueprints.main import routes
        from app.blueprints.auth import routes
        from app.blueprints.optimization import routes
        from app.blueprints.prediction import routes
        from app.blueprints.segmentation import routes

        # Register blueprints
        from app.blueprints.main import main_bp
        from app.blueprints.auth import auth_bp
        from app.blueprints.optimization import optimization_bp
        from app.blueprints.prediction import prediction_bp
        from app.blueprints.segmentation import segmentation_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(optimization_bp)
        app.register_blueprint(prediction_bp)
        app.register_blueprint(segmentation_bp)

    return app
