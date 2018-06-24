import pytest
from server import backend

@pytest.fixture
def app():
    flask_app = backend.create_app("server.config.TestingConfig")
    return flask_app
