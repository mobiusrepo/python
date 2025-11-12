from fastapi import APIRouter
from models.opportunity_cost_model import OpportunityCostRequest, OpportunityCostResponse
from services.opportunity_cost_service import opportunity_cost_service

router = APIRouter()

@router.post("/opportunity-cost", response_model=OpportunityCostResponse)
def opportunity_cost(request: OpportunityCostRequest):
    return opportunity_cost_service(request)
