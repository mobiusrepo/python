from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Tuple

class Outcome(BaseModel):
    id: str
    value: float
    # Add other attributes that might be in an outcome, e.g., attention_cost
    attention_cost: Optional[float] = None

class ComputeUtilityRequest(BaseModel):
    agent_preferences: Dict[str, float] = Field(..., description="Dictionary of agent preferences for different outcome attributes.")
    outcome_set: List[Outcome] = Field(..., description="List of outcomes, each with an 'id' and other attributes.")
    normalize: bool = True
    normalization_method: str = Field("minmax", description="'minmax' or 'zscore'.")
    attention_attr: Optional[str] = Field(None, description="Attribute to use for attention cost (e.g., 'attention_cost').")
    attention_budget: Optional[float] = Field(None, description="Budget for attention.")
    attention_cost_coeff: float = 1.0
    softmax_temp: float = 1.0
    satisficing_threshold: Optional[float] = Field(None, description="Threshold for satisficing.")
    apply_attention: bool = True

class Choice(BaseModel):
    id: str
    score: float

class ComputeUtilityResponse(BaseModel):
    raw: Dict[str, float]
    penalized: Dict[str, float]
    normalized: Dict[str, float]
    probabilities: Dict[str, float]
    choice: Choice
