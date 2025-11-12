from fastapi import APIRouter
from models.bounded_rationality_model import BoundedRationalityRequest, BoundedRationalityResponse
from services.bounded_rationality_service import bounded_rationality_service

router = APIRouter()

@router.post("/bounded-rationality", response_model=BoundedRationalityResponse)
def bounded_rationality(request: BoundedRationalityRequest):
    return bounded_rationality_service(request)
