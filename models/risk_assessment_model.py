from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class RiskAssessmentRequest(BaseModel):
    choice_set: List[str] = Field(..., description="List of choice names.")
    payoff_matrix: Dict[str, float] = Field(..., description="Dictionary of payoffs per choice.")
    prob_matrix: Optional[List[List[float]]] = Field(None, description="Optional transition/probability matrix (Markov).")
    confidence: float = Field(0.95, description="Confidence level for interval.")

class RiskMetrics(BaseModel):
    ExpectedValue: float
    ConfidenceInterval: float
    RiskAdjustedValue: float

class RiskAssessmentResponse(BaseModel):
    risk_profile: Dict[str, RiskMetrics]
