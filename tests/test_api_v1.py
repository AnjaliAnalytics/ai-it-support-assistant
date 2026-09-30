from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_missing_incident_404():
    """Verify 404 response for non-existent incident lookup."""
    response = client.get("/api/v1/incidents/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_invalid_incident_creation_payload():
    """Verify validation error (422) for missing mandatory fields."""
    payload = {"title": "Short"}  # Title too short and missing description
    response = client.post("/api/v1/incidents", json=payload)
    assert response.status_code == 422


def test_analytics_summary_endpoint():
    """Verify analytics endpoint returns summary metrics."""
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_incidents" in data
    assert "total_knowledge_articles" in data
    assert "incidents_by_priority" in data