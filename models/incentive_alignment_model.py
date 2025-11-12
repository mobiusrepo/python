from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class IncentiveAlignmentRequest(BaseModel):
    choice_set: List[str] = Field(..., description="List of possible actions/choices.")
    payoff_matrix: Dict[str, float] = Field(..., description="Agent-specific payoffs per choice.")
    global_target: Optional[float] = Field(None, description="Optional global payoff goal to align with.")
    epsilon: float = Field(1e-3, description="Small relaxation for constraints.")

class IncentiveAlignmentResponse(BaseModel):
    updated_strategy: Dict[str, float]
    expected_payoff: float
    target_satisfied: bool
