from models.payoff_weighted_aggregation_model import PayoffWeightedAggregationRequest, PayoffWeightedAggregationResponse
from typing import Dict, Any

def payoff_weighted_aggregation_service(request: PayoffWeightedAggregationRequest) -> PayoffWeightedAggregationResponse:
    proposal_map = request.proposal_map
    payoff_gradients = request.payoff_gradients

    # --- Compute weighted scores ---
    weighted_scores = {}
    for k, v in proposal_map.items():
        if isinstance(v, dict):
            v = v.get("amount", 0.0)
        weight = payoff_gradients.get(k, 1.0)
        weighted_scores[k] = float(v) * float(weight)

    # --- Normalize to probabilities (consensus) ---
    total = sum(weighted_scores.values())
    consensus = {k: (v / total if total > 0 else 0.0) for k, v in weighted_scores.items()}

    # --- Find winning pattern ---
    winning_pattern = max(weighted_scores, key=weighted_scores.get) if weighted_scores else ""

    print(f"Payoff Weighted Aggregation: Winning Pattern={winning_pattern}, Consensus={consensus}, Weighted Scores={weighted_scores}")
    return PayoffWeightedAggregationResponse(
        winning_pattern=winning_pattern,
        consensus_dsl=consensus,
        weighted_scores=weighted_scores
    )
