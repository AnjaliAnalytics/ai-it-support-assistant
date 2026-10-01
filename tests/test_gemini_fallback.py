from unittest.mock import patch
from backend.app.services.gemini_service import GeminiService


def test_gemini_fallback_when_api_fails():
    """Verify GeminiService returns structured fallback data when any LLM API call raises an Exception."""
    kb_articles = [
        {
            "id": "1",
            "title": "VPN Troubleshooting",
            "content": "Check network connection and restart Cisco AnyConnect client.",
            "category": "Network",
            "relevance_score": 0.85,
        }
    ]

    # Force the API call to fail so the fallback handler executes
    with patch("google.genai.Client", side_effect=Exception("API Quota Exceeded")):
        result = GeminiService.generate_incident_analysis(
            title="VPN Connection Failure",
            description="User cannot connect to Mumbai VPN gateway.",
            category="Network",
            predicted_priority="P2",
            ml_confidence=0.91,
            kb_articles=kb_articles,
        )

        # Assert fallback structure matching generate_fallback_response() keys
        assert result["fallback_used"] is True
        assert "summary" in result
        assert "recommended_steps" in result
        assert isinstance(result["recommended_steps"], list)
        assert len(result["recommended_steps"]) > 0
        assert "evidence_used" in result