from main import app
from fastapi.testclient import TestClient


api_endpoint = "/api/auth"
client = TestClient(app)


def test_register_account():
    response = client.post(
        f"{api_endpoint}/register/",
        json={
            "name": "pytest用",
            "password": "pytest",
        })
    assert response.status_code == 201
