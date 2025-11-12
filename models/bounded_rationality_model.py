from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class BoundedRationalityRequest(BaseModel):
    choice_set: List[str] = Field(..., description="List of option names.")
    payoff_matrix: Dict[str, float] = Field(..., description="Dictionary of option to payoff (expected utility).")
    agent_capacity: Dict[str, float] = Field({}, description="Dictionary describing agent capacity (e.g., {'max_evals': 5, 'attention': 1.0}).")
    decision_tree: Optional[Dict[str, Any]] = Field(None, description="Optional structure describing ordering / branches.")
    mode: str = Field("satisficing", description="Mode: 'satisficing' | 'simulate' | 'bayes'.")
    aspiration: Optional[float] = Field(None, description="Payoff threshold for satisficing. If None, set to median payoff.")
    sample_budget: int = Field(5, description="Number of candidate evaluations allowed.")
    random_seed: Optional[int] = Field(None, description="Optional seed for reproducibility.")

class BoundedRationalityResponse(BaseModel):
    simplified_choice: Optional[str]
    heuristic_trace: List[Dict[str, Any]]
