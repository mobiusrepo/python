from fastapi import APIRouter
from models.incentive_alignment_model import IncentiveAlignmentRequest, IncentiveAlignmentResponse
from services.incentive_alignment_service import incentive_alignment_service

router = APIRouter()

@router.post("/incentive-alignment", response_model=IncentiveAlignmentResponse)
def incentive_alignment(request: IncentiveAlignmentRequest):
    return incentive_alignment_service(request)
