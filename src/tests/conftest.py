import pytest
from server import backend

@pytest.fixture
def app():
    return backend.app
