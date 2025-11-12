from models.efficiency_ranking_model import EfficiencyRankingRequest, EfficiencyRankingResponse
import numpy as np
import pandas as pd
from scipy.stats import entropy
from typing import Dict, List, Any, Optional

class EfficiencyRanker:
    def __init__(self):
        self.ranked_list: List[str] = []
        self.preferred_variant: Optional[str] = None

    def efficiencyRanking(
        self,
        candidate_set: List[str],
        usage_trace: Dict[str, List[float]],
        payoff_vector: Dict[str, float]
    ) -> Dict[str, Any]:
        efficiency_scores = {}
        for candidate in candidate_set:
            usage = np.array(usage_trace.get(candidate, [1.0]))
            prob_usage = usage / usage.sum() if usage.sum() > 0 else np.ones_like(usage) / len(usage)
            ent = entropy(prob_usage)
            payoff = payoff_vector.get(candidate, 0.0)
            denom = max(float(ent), 1e-3)
            efficiency_scores[candidate] = payoff / denom

        ranked_list = sorted(efficiency_scores, key=lambda x: efficiency_scores[x], reverse=True)
        preferred_variant = ranked_list[0] if ranked_list else None

        self.ranked_list = ranked_list
        self.preferred_variant = preferred_variant

        return {
            "RankedList": ranked_list,
            "PreferredVariant": preferred_variant,
            "EfficiencyScores": {k: float(v) for k,v in efficiency_scores.items()}
        }

def efficiency_ranking_service(request: EfficiencyRankingRequest) -> EfficiencyRankingResponse:
    ranker = EfficiencyRanker()
    result = ranker.efficiencyRanking(
        candidate_set=request.candidate_set,
        usage_trace=request.usage_trace,
        payoff_vector=request.payoff_vector
    )

    print(f"Efficiency Ranking: {result}")
    return EfficiencyRankingResponse(
        ranked_list=result["RankedList"],
        preferred_variant=result["PreferredVariant"],
        efficiency_scores=result["EfficiencyScores"]
    )
