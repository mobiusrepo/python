from pydantic import BaseModel, Field
from typing import Dict, Any

class PayoffWeightedAggregationRequest(BaseModel):
    proposal_map: Dict[str, Any] = Field(..., description="Map of proposals, e.g., {option_name: value}")
    payoff_gradients: Dict[str, float] = Field(..., description="Map of payoff gradients (weights) per proposal, e.g., {option_name: weight}")

class PayoffWeightedAggregationResponse(BaseModel):
    winning_pattern: str
    consensus_dsl: Dict[str, float]
    weighted_scores: Dict[str, float]
