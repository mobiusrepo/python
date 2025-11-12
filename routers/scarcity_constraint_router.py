from fastapi import APIRouter
from models.scarcity_constraint_model import ScarcityConstraintRequest, ScarcityConstraintResponse
from services.scarcity_constraint_service import scarcity_constraint_service

router = APIRouter()

@router.post("/scarcity-constraint", response_model=ScarcityConstraintResponse)
def scarcity_constraint(request: ScarcityConstraintRequest):
    return scarcity_constraint_service(request)
