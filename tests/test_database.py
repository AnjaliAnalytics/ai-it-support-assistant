from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_and_read_incident():
    payload = {
        "title": "Test VPN Connectivity Ticket",
        "description": "User cannot connect to VPN network from remote location.",
        "category": "Network",
        "priority": "High",
    }
    response = client.post("/api/v1/incidents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data

    # Test List Incidents
    list_response = client.get("/api/v1/incidents")
    assert list_response.status_code == 200
    assert len(list_response.json()) > 0