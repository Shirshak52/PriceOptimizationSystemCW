from flask import Flask
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
    app.jinja_loader.searchpath.append("app/blueprints/auth/templates")
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
        from app.blueprints.auth.routes import login, logout

        # Register blueprints
        from app.blueprints.main import main_bp
        from app.blueprints.auth import auth_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

    return app
