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


def test_login():
    response = client.post(
        f"{api_endpoint}/login/",
        json={
            "username": "pytest用",
            "password": "pytest",
        })
    response_json = response.json()
    print(response.json())
    assert response.status_code == 200
    assert response_json["access_token"] is not None
