from os import environ, path
from dotenv import load_dotenv

# Specify a '.env' file containing key/value config values
basedir = path.abspath(path.join(path.dirname(__file__), ".."))
load_dotenv(path.join(basedir, ".env"))
# print(f"Loading .env from: {path.join(basedir, '.env')}")


class Config:
    """Set Flask application configuration variables."""

    # General config values
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Database config values
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

    # Flask-Security config values
    SECURITY_PASSWORD_SALT = environ.get("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = environ.get("SECURITY_PASSWORD_HASH")
    SECURITY_REGISTERABLE = environ.get("SECURITY_REGISTERABLE")
    SECURITY_SEND_PASSWORD_RESET_EMAIL = environ.get(
        "SECURITY_SEND_PASSWORD_RESET_EMAIL"
    )
    # SECURITY_LOGIN_URL = environ.get("SECURITY_LOGIN_URL")
    # SECURITY_LOGIN_USER_TEMPLATE = environ.get("SECURITY_LOGIN_USER_TEMPLATE")
