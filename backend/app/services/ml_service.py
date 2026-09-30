import os
import joblib
import pandas as pd
from backend.app.core.logging_config import logger


class MLService:
    _instance = None
    _model = None

    MODEL_VERSION = "1.0.0-logistic-regression"
    ARTIFACT_PATH = os.path.join("backend", "app", "ml", "artifacts", "priority_model.joblib")

    @classmethod
    def get_model(cls):
        if cls._model is None:
            if not os.path.exists(cls.ARTIFACT_PATH):
                logger.warning(f"Model artifact not found at {cls.ARTIFACT_PATH}. Training emergency inline model...")
                from backend.app.ml.train import train_model
                train_model()

            logger.info(f"Loading ML model artifact from {cls.ARTIFACT_PATH}...")
            cls._model = joblib.load(cls.ARTIFACT_PATH)
            logger.info("ML model loaded successfully into memory.")
        return cls._model

    @classmethod
    def predict_priority(
        cls,
        description: str,
        category: str = "Unassigned",
        system_criticality: str = "Medium",
        affected_users: int = 1
    ) -> dict:
        model = cls.get_model()

        input_df = pd.DataFrame([{
            "description": description,
            "category": category,
            "system_criticality": system_criticality,
            "affected_users": affected_users,
            "description_length": len(description)
        }])

        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        confidence = float(max(probabilities))

        return {
            "predicted_priority": prediction,
            "confidence": round(confidence, 4),
            "model_version": cls.MODEL_VERSION
        }