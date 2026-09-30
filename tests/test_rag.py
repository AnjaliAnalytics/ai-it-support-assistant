from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_kb_search_endpoint():
    payload = {
        "query": "VPN connection failure or remote authentication problem",
        "top_k": 3
    }
    response = client.post("/api/v1/knowledge/search", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "total_results" in data
    assert "articles" in data
    assert isinstance(data["articles"], list)