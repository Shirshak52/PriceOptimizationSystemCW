import pytest
from app import create_app, db
from app.config import TestingConfig


@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        yield app


@pytest.fixture
def db_session(app):
    db.create_all()
    yield db.session

    db.session.remove()
    db.drop_all()
