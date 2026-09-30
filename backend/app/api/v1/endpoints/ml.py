from fastapi import APIRouter, HTTPException, status
from backend.app.models.pydantic_models import MLPredictRequest, MLPredictResponse
from backend.app.services.ml_service import MLService

router = APIRouter()


@router.post("/ml/predict-priority", response_model=MLPredictResponse, status_code=status.HTTP_200_OK)
def predict_priority(request: MLPredictRequest):
    """
    Predict IT Incident Priority (P1, P2, P3, P4) using Scikit-Learn Logistic Regression model.
    """
    try:
        result = MLService.predict_priority(
            description=request.description,
            category=request.category,
            system_criticality=request.system_criticality,
            affected_users=request.affected_users
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Machine Learning prediction error: {str(e)}"
        )