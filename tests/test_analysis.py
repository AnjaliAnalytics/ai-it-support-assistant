from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_ai_analysis_endpoint():
    payload = {
        "title": "VPN connection drops",
        "description": "User experiences continuous disconnection from Cisco AnyConnect VPN.",
        "category": "Network",
        "system_criticality": "High",
        "affected_users": 50
    }
    response = client.post("/api/v1/analysis/resolve", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_priority" in data
    assert "recommended_steps" in data
    assert "evidence_used" in data
    assert isinstance(data["recommended_steps"], list)