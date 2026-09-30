from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_predict_priority_endpoint():
    payload = {
        "description": "Entire office internet router failure and network outage.",
        "category": "Network",
        "system_criticality": "Critical",
        "affected_users": 300
    }
    response = client.post("/api/v1/ml/predict-priority", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_priority"] in ["P1", "P2", "P3", "P4"]
    assert "confidence" in data
    assert data["confidence"] > 0.0
    assert "model_version" in data