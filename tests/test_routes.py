import pytest
from core.server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_root_route(client):
    response = client.get("/")
    assert response.status_code == 200

