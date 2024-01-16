import pytest
from core.libs.exceptions import FyleError
from core.server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_fyle_error_handling(client):
    with pytest.raises(FyleError) as excinfo:
        raise FyleError(404, "Not Found")
    assert excinfo.value.status_code == 404
    assert excinfo.value.message == "Not Found"

def test_http_exception_handling(client):
    response = client.get("/nonexistent-route")
    assert response.status_code == 404
    assert response.json == {"error": "NotFound", "message": "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}


def test_fyle_error_to_dict():
    error = FyleError(401, "Unauthorized")
    error_dict = error.to_dict()

    assert error_dict == {"message": "Unauthorized"}

