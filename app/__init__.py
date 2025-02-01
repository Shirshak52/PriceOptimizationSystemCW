from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_migrate import Migrate
from app.config import Config

# Initialize addon instances
db = SQLAlchemy()
migrate = Migrate()
security = Security()


def create_app():
    # Create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.Branch.model import Branch

    user_datastore = SQLAlchemyUserDatastore(db, Branch, None)
    security.init_app(app, user_datastore)

    # Within the app context
    with app.app_context():

        # Import model classes for migration
        from app.models.Supermarket.model import Supermarket
        from app.models.DatasetFile.model import DatasetFile
        from app.models.Optimization.model import Optimization
        from app.models.Prediction.model import Prediction
        from app.models.Segmentation.model import Segmentation
        from app.models.Cluster.model import Cluster

        # Setup admin views

        # Import routes
        from app.blueprints.main.routes import index
        from app.blueprints.login.routes import login

        # Register blueprints
        from app.blueprints.main import main_bp
        from app.blueprints.login import login_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(login_bp)

    return app
