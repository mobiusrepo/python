from pydantic import BaseModel, Field
from typing import Dict, Any

class AgentEconomicMetrics(BaseModel):
    benefit: float
    cost: float
    capability: float
    tokenFlow: float

class AggregateWeightedChoiceRequest(BaseModel):
    economic_values: Dict[str, AgentEconomicMetrics] = Field(..., description="Dictionary of agent economic metrics, e.g., {agent_name: {'benefit': float, 'cost': float, 'capability': float, 'tokenFlow': float}}")

class AggregateWeightedChoiceResponse(BaseModel):
    group_decision_score: float
    avg_capability: float
    avg_tokenFlow: float
    agent_contributions: Dict[str, AgentEconomicMetrics]
