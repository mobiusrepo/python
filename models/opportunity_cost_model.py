from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class OpportunityCostRequest(BaseModel):
    choice_set: List[str] = Field(..., description="List of choice names.")
    payoff_matrix: Dict[str, float] = Field(..., description="Dictionary of payoffs per choice.")
    P: Optional[List[List[float]]] = Field(None, description="Optional Markov transition matrix.")

class OpportunityCostResponse(BaseModel):
    trade_off_profile: Dict[str, Dict[str, float]]
