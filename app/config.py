from os import environ, path
from dotenv import load_dotenv

# Specify a '.env' file containing key/value config values
basedir = path.abspath(path.join(path.dirname(__file__), ".."))
load_dotenv(path.join(basedir, ".env"))
# print(f"Loading .env from: {path.join(basedir, '.env')}")


class Config:
    """Set Flask application configuration variables."""

    # General config values
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Datasetfile-related config values
    UPLOAD_FOLDER_OPTIMIZATION = environ.get("UPLOAD_FOLDER_OPTIMIZATION")
    UPLOAD_FOLDER_PREDICTION = environ.get("UPLOAD_FOLDER_PREDICTION")
    UPLOAD_FOLDER_SEGMENTATION = environ.get("UPLOAD_FOLDER_SEGMENTATION")
    MAX_CONTENT_LENGTH = int(environ.get("MAX_CONTENT_LENGTH"))

    # ML processing-related config values
    MODELS_FOLDER_PREDICTION = path.abspath(
        path.join(basedir, environ.get("MODELS_FOLDER_PREDICTION"))
    )

    # Flask-session config values
    SESSION_TYPE = environ.get("SESSION_TYPE")
    SESSION_FILE_DIR = environ.get("SESSION_FILE_DIR")
    SESSION_PERMANENT = environ.get("SESSION_PERMANENT")

    # Database config values
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
