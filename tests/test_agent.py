from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_agent_initial_step():
    payload = {
        "title": "VPN connected but internal site fails",
        "description": "User can connect to VPN successfully, but internal HR site gives DNS error.",
        "category": "Network",
        "user_feedback": "",
        "conversation_history": []
    }
    response = client.post("/api/v1/agent/step", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == 1
    assert "recommended_action" in data
    assert "evidence_retrieved" in data
    assert isinstance(data["evidence_retrieved"], list)


def test_agent_followup_escalation_step():
    payload = {
        "title": "VPN connected but internal site fails",
        "description": "User can connect to VPN successfully, but internal HR site gives DNS error.",
        "category": "Network",
        "user_feedback": "Flushed DNS cache and restarted router, but the site still fails to load.",
        "conversation_history": ["Step 1: Flush DNS cache"]
    }
    response = client.post("/api/v1/agent/step", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["current_step"] == 2
    assert data["escalation_recommended"] is True
    assert data["status"] == "ESCALATED"