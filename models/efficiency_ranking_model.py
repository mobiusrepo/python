from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class EfficiencyRankingRequest(BaseModel):
    candidate_set: List[str] = Field(..., description="List of candidate options.")
    usage_trace: Dict[str, List[float]] = Field(..., description="Dictionary mapping each candidate to its usage history/probabilities.")
    payoff_vector: Dict[str, float] = Field(..., description="Dictionary mapping each candidate to expected payoff.")

class EfficiencyRankingResponse(BaseModel):
    ranked_list: List[str]
    preferred_variant: Optional[str]
    efficiency_scores: Dict[str, float]
