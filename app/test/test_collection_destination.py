from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

api_endpoint = "/api/collection_destination"


def test_register_collection_destination():
    response = client.post(
        f"{api_endpoint}/register/",
        json={
            "name": "pytest用",
            "domain": "example.com",
            "contents_attr_name": "contents-attr-name-test",
            "title_attr_name": "title-attr-name-test",
            "published_date_attr_name": "published-date-attr-name-test",
            "content_url_attr_name": "content-url-attr-name",
            "account_id": 1
        })
    assert response.status_code == 201


def test_get_collection_destination_list():
    response = client.get(f"{api_endpoint}/list/")
    res_json = response.json()
    assert response.status_code == 200
    assert len(res_json) > 0


def test_get_collection_destination():
    response = client.get(f"{api_endpoint}/1")
    res_json = response.json()
    assert response.status_code == 200
    assert res_json["name"] == "pytest用"


def test_delete_collection_destination():
    response = client.delete(f"{api_endpoint}/1")
    assert response.status_code == 204
