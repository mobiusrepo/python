from pydantic import BaseModel, Field
from typing import Dict, Any, List

class ScarcityConstraintRequest(BaseModel):
    resource_pool: Dict[str, float] = Field(..., description="Available resources, e.g., {'resourceA': 100.0}")
    demand_vector: Dict[str, Dict[str, float]] = Field(..., description="Demands for resources per option, e.g., {'option1': {'resourceA': 10.0}}")

class ScarcityConstraintResponse(BaseModel):
    constraint_set: Dict[str, bool]
    feasibility_map: Dict[str, float]
    infeasible_options: List[str]
    binding_constraints: Dict[str, List[str]]
