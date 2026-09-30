from backend.app.core.database import SessionLocal, init_db
from backend.app.core.logging_config import logger
from backend.app.models.db_models import Incident, KnowledgeArticle


def seed_database():
    init_db()
    db = SessionLocal()

    try:
        # Check if DB is already seeded
        if db.query(KnowledgeArticle).count() > 0:
            logger.info("Database already seeded. Skipping.")
            return

        logger.info("Seeding synthetic Knowledge Base articles...")
        kb_articles = [
            KnowledgeArticle(
                title="VPN Connection Failure Guide",
                category="Network",
                content="Ensure Cisco AnyConnect client is updated. Verify MFA token synchronization. Clear DNS cache using 'ipconfig /flushdns'.",
            ),
            KnowledgeArticle(
                title="Outlook Prompting Password Continuously",
                category="Authentication",
                content="Open Windows Credential Manager. Remove stored MS Outlook credentials under Windows Credentials. Restart Outlook and re-authenticate.",
            ),
            KnowledgeArticle(
                title="Self-Service Password Reset (SSPR) Steps",
                category="Authentication",
                content="Navigate to identity.company.com. Click 'Forgot Password'. Complete Authenticator app push notification to verify identity.",
            ),
            KnowledgeArticle(
                title="Citrix Workspace Display Resolution Bug",
                category="Application Access",
                content="Right-click Citrix Workspace icon in system tray -> Advanced Preferences -> High DPI setting -> Select 'No, use native resolution'.",
            ),
            KnowledgeArticle(
                title="Wi-Fi Authentication Error on Corporate Network",
                category="Network",
                content="Forget 'Corporate-Secure' network in Wi-Fi settings. Re-select network, set EAP method to PEAP, Phase 2 authentication to MSCHAPv2.",
            ),
        ]
        db.add_all(kb_articles)

        logger.info("Seeding sample synthetic Incidents...")
        sample_incidents = [
            Incident(
                title="Cannot connect to Cisco VPN",
                description="User receives timeout error when connecting to Mumbai VPN gateway.",
                category="Network",
                priority="High",
                status="OPEN",
            ),
            Incident(
                title="Outlook repeatedly asks for password",
                description="Outlook desktop app keeps popping up login window despite entering correct password.",
                category="Authentication",
                priority="Medium",
                status="OPEN",
            ),
        ]
        db.add_all(sample_incidents)

        db.commit()
        logger.info("Synthetic database seeding completed successfully!")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()