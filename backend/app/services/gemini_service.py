import json
from typing import Dict, Any, List
from google import genai
from google.genai import types
from backend.app.core.config import settings
from backend.app.core.logging_config import logger


SYSTEM_PROMPT = """You are an expert IT Support Specialist AI.
Your task is to analyze IT incidents based strictly on the provided Grounded Evidence (Knowledge Base Articles) and ML Predictions.

STRICT SAFETY & OPERATIONAL RULES:
1. Use ONLY supplied evidence and standard IT troubleshooting logic.
2. Do NOT invent internal company infrastructure or URLs.
3. Keep recommended steps safe, actionable, and sequential.
4. Recommend escalation to Tier 2/3 engineering if evidence is insufficient or if priority is P1/P2 with high user impact.
5. Return output STRICTLY in valid JSON matching the requested schema.
"""


class GeminiService:
    @staticmethod
    def generate_incident_analysis(
        title: str,
        description: str,
        category: str,
        predicted_priority: str,
        ml_confidence: float,
        kb_articles: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Sends grounded incident evidence to Gemini and generates structured resolution steps.
        Includes robust error handling and fallback mechanism.
        """
        api_key = settings.GEMINI_API_KEY

        # Grounding evidence context preparation
        kb_context_str = "\n".join([
            f"- Article [{a['id']}]: '{a['title']}' (Category: {a['category']}) -> Content: {a['content']}"
            for a in kb_articles
        ]) if kb_articles else "No matching knowledge base articles found."

        user_prompt = f"""
INCIDENT DETAILS:
- Title: {title}
- Description: {description}
- Category: {category}
- ML Predicted Priority: {predicted_priority} (Confidence: {ml_confidence})

GROUNDED KNOWLEDGE BASE EVIDENCE (RAG Context):
{kb_context_str}

Analyze this incident and respond strictly in JSON format with the following keys:
"summary", "category_explanation", "priority_explanation", "recommended_steps" (list), "evidence_used" (list), "possible_cause", "escalation_needed" (boolean), "confidence", "limitations".
"""

        if not api_key or api_key == "AIzaSyYourActualGeminiApiKeyHere" or len(api_key) < 10:
            logger.warning("GEMINI_API_KEY not configured or invalid. Using structured static fallback.")
            return GeminiService._get_fallback_analysis(predicted_priority, kb_articles)

        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            parsed_res = json.loads(response.text)
            parsed_res["fallback_used"] = False
            return parsed_res

        except Exception as e:
            logger.error(f"Gemini API invocation failed: {e}. Executing safe fallback response.")
            return GeminiService._get_fallback_analysis(predicted_priority, kb_articles)

    @staticmethod
    def _get_fallback_analysis(priority: str, kb_articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        evidence = [a['title'] for a in kb_articles] if kb_articles else ["Standard ITIL Incident Handling Matrix"]
        steps = [a['content'] for a in kb_articles] if kb_articles else [
            "Verify network physical/wireless layer connectivity.",
            "Clear DNS cache and flush active credentials.",
            "Contact IT Service Desk if issue persists after restart."
        ]
        return {
            "summary": "Automated analysis generated via local grounded Knowledge Base fallback.",
            "category_explanation": "Categorized based on primary symptom analysis.",
            "priority_explanation": f"Priority assigned as {priority} by local Scikit-Learn classifier.",
            "recommended_steps": steps,
            "evidence_used": evidence,
            "possible_cause": "System connection or credential sync issue.",
            "escalation_needed": priority in ["P1", "P2"],
            "confidence": "Medium (Fallback Mode)",
            "limitations": "Gemini LLM service was unreachable; analysis relied strictly on rule-based KB matching.",
            "fallback_used": True
        }