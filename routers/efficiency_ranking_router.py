from fastapi import APIRouter
from models.efficiency_ranking_model import EfficiencyRankingRequest, EfficiencyRankingResponse
from services.efficiency_ranking_service import efficiency_ranking_service

router = APIRouter()

@router.post("/efficiency-ranking", response_model=EfficiencyRankingResponse)
def efficiency_ranking(request: EfficiencyRankingRequest):
    return efficiency_ranking_service(request)
