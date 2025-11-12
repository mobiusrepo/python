from fastapi import APIRouter
from models.compute_utility_model import ComputeUtilityRequest, ComputeUtilityResponse
from services.compute_utility_service import compute_utility_service

router = APIRouter()

@router.post("/compute-utility", response_model=ComputeUtilityResponse)
def compute_utility(request: ComputeUtilityRequest):
    return compute_utility_service(request)
