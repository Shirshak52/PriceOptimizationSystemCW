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
    UPLOAD_FOLDER = environ.get("UPLOAD_FOLDER")
    # UPLOAD_FOLDER = environ.get(path.join(basedir, "uploads"))
    MAX_CONTENT_LENGTH = int(environ.get("MAX_CONTENT_LENGTH"))

    # Database config values
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = environ.get("SQLALCHEMY_ECHO")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

    # Celery config values
    CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = environ.get("CELERY_RESULT_BACKEND")
    CELERY_ACCEPT_CONTENT = environ.get("CELERY_ACCEPT_CONTENT")
    CELERY_TASK_SERIALIZER = environ.get("CELERY_TASK_SERIALIZER")

    print(CELERY_ACCEPT_CONTENT)
