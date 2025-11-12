from fastapi import APIRouter
from models.risk_assessment_model import RiskAssessmentRequest, RiskAssessmentResponse
from services.risk_assessment_service import risk_assessment_service

router = APIRouter()

@router.post("/risk-assessment", response_model=RiskAssessmentResponse)
def risk_assessment(request: RiskAssessmentRequest):
    return risk_assessment_service(request)
