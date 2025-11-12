from fastapi import APIRouter
from models.aggregate_weighted_choice_model import AggregateWeightedChoiceRequest, AggregateWeightedChoiceResponse
from services.aggregate_weighted_choice_service import aggregate_weighted_choice_service

router = APIRouter()

@router.post("/aggregate-weighted-choice", response_model=AggregateWeightedChoiceResponse)
def aggregate_weighted_choice(request: AggregateWeightedChoiceRequest):
    return aggregate_weighted_choice_service(request)
