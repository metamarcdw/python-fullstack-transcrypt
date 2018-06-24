import os
import pytest
from server import backend

@pytest.fixture
def app():
    os.environ["TODOS_FS_MODE"] = "testing"
    flask_app = backend.create_app()
    return flask_app
