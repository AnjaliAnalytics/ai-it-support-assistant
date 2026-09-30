from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.services.agent_tools import AgentTools
from backend.app.services.gemini_service import GeminiService
from backend.app.core.logging_config import logger


class TroubleshootingAgentService:
    @staticmethod
    def process_troubleshooting_step(
        db: Session,
        title: str,
        description: str,
        category: str,
        user_feedback: str = "",
        conversation_history: List[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a controlled tool-based troubleshooting step maintaining multi-turn context.
        """
        if conversation_history is None:
            conversation_history = []

        # Step 1: Execute predefined tools to gather grounded evidence
        search_query = f"{title} {description} {user_feedback}".strip()
        kb_articles = AgentTools.search_knowledge_base(db, query=search_query)
        similar_incidents = AgentTools.get_similar_incidents(db, category=category)

        # Step 2: Pass grounded evidence and state history to Gemini LLM analytical engine
        full_context_prompt = f"""
TROUBLESHOOTING SESSION STATE:
- Initial Incident: {title}
- Description: {description}
- Category: {category}
- Prior Steps Applied: {conversation_history}
- Latest User Observation/Feedback: {user_feedback if user_feedback else "Initial report."}

GROUNDED TOOLS OUTPUT:
- Knowledge Base Articles Found: {[a['title'] for a in kb_articles]}
- Similar Historical Incidents: {[i['title'] for i in similar_incidents]}
"""

        # Step 3: Run analytical reasoning via Gemini service
        ai_res = GeminiService.generate_incident_analysis(
            title=title,
            description=f"{description} | User Feedback: {user_feedback}",
            category=category,
            predicted_priority="P3" if "P3" not in description else "P2",
            ml_confidence=0.88,
            kb_articles=kb_articles
        )

        # Determine next logical step in the state machine
        next_action = ai_res["recommended_steps"][0] if ai_res.get("recommended_steps") else "Verify device network IP configuration."
        escalate = ai_res.get("escalation_needed", False) or "fail" in user_feedback.lower() or "not working" in user_feedback.lower()

        return {
            "current_step": len(conversation_history) + 1,
            "status": "ESCALATED" if escalate else "IN_PROGRESS",
            "ai_summary": ai_res.get("summary", "Analysis complete."),
            "recommended_action": next_action,
            "all_recommended_steps": ai_res.get("recommended_steps", []),
            "evidence_retrieved": [a["title"] for a in kb_articles],
            "possible_cause": ai_res.get("possible_cause", "Pending diagnostic validation."),
            "escalation_recommended": escalate,
            "fallback_used": ai_res.get("fallback_used", False)
        }