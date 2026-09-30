from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["ok", "healthy"]


def test_list_incidents_endpoint():
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)