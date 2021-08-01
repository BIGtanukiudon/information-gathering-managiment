from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

api_endpoint = "/api/content"


def test_scraping_contents():
    response = client.post(f"{api_endpoint}/scraping_contents/")
    # res_json = response.json()
    assert response.status_code == 200


def test_get_content_list():
    response = client.get(f"{api_endpoint}/list/30")
    res_json = response.json()
    assert response.status_code == 200
    assert len(res_json) > 0


def test_test_scraping_contents():
    response = client.post(
        f"{api_endpoint}/test_scraping_contents/",
        json={
            "name": "test",
            "domain": "domain",
            "contents_attr_name": "contents_attr_name",
            "title_attr_name": "title_attr_name",
            "published_date_attr_name": "published_date_attr_name",
            "content_url_attr_name": "content_url_attr_name",
            "account_id": 1})
    res_json = response.json()
    assert response.status_code == 200
    assert len(res_json) > 0
