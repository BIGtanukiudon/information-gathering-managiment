from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

api_endpoint = "/api/content"


def test_scraping_contents():
    response = client.post(f"{api_endpoint}/scraping_contents/")
    # res_json = response.json()
    assert response.status_code == 200
