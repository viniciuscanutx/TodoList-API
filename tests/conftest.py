import pytest
from fastapi.testclient import TestClient

from fastapiproj.app import app


@pytest.fixture
def client():
    return TestClient(app)
