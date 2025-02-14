import pytest
from fastapi.testclient import TestClient

from core.app.create_app import create_application


@pytest.fixture(scope="function")
def client():
    app = create_application()
    with TestClient(app) as client:
        yield client
