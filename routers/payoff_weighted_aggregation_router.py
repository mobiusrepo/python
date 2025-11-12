from fastapi import APIRouter
from models.payoff_weighted_aggregation_model import PayoffWeightedAggregationRequest, PayoffWeightedAggregationResponse
from services.payoff_weighted_aggregation_service import payoff_weighted_aggregation_service

router = APIRouter()

@router.post("/payoff-weighted-aggregation", response_model=PayoffWeightedAggregationResponse)
def payoff_weighted_aggregation(request: PayoffWeightedAggregationRequest):
    return payoff_weighted_aggregation_service(request)
