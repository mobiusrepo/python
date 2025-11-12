from models.aggregate_weighted_choice_model import AggregateWeightedChoiceRequest, AggregateWeightedChoiceResponse, AgentEconomicMetrics
from typing import List, Dict, Any

def aggregate_weighted_choice_service(request: AggregateWeightedChoiceRequest) -> AggregateWeightedChoiceResponse:
    economic_values = request.economic_values

    if not economic_values:
        return AggregateWeightedChoiceResponse(
            group_decision_score=0.0,
            avg_capability=0.0,
            avg_tokenFlow=0.0,
            agent_contributions={}
        )

    total_benefit = sum(v.benefit for v in economic_values.values())
    total_cost = sum(v.cost for v in economic_values.values())
    total_capability = sum(v.capability for v in economic_values.values())
    total_tokenFlow = sum(v.tokenFlow for v in economic_values.values())
    n_agents = len(economic_values)

    group_decision_score = (total_benefit - total_cost) / max(total_benefit + total_cost, 1e-6)
    avg_capability = total_capability / n_agents
    avg_tokenFlow = total_tokenFlow / n_agents

    return AggregateWeightedChoiceResponse(
        group_decision_score=group_decision_score,
        avg_capability=avg_capability,
        avg_tokenFlow=avg_tokenFlow,
        agent_contributions=economic_values
    )
