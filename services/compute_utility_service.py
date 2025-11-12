from models.compute_utility_model import ComputeUtilityRequest, ComputeUtilityResponse, Outcome, Choice
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

class ComputeUtility:
    def __init__(
        self,
        normalize: bool = True,
        normalization_method: str = "minmax",
        attention_attr: Optional[str] = None,
        attention_budget: Optional[float] = None,
        attention_cost_coeff: float = 1.0,
        softmax_temp: float = 1.0,
        satisficing_threshold: Optional[float] = None,
        eps: float = 1e-9
    ):
        self.normalize = normalize
        self.normalization_method = normalization_method
        self.attention_attr = attention_attr
        self.attention_budget = attention_budget
        self.attention_cost_coeff = attention_cost_coeff
        self.softmax_temp = softmax_temp
        self.satisficing_threshold = satisficing_threshold
        self.eps = eps

    def compute_raw(self, agent_preferences: Dict[str, float], outcome_set: List[Outcome]) -> Dict[str, float]:
        raw = {}
        for o in outcome_set:
            oid = o.id
            u = 0.0
            for attr, w in agent_preferences.items():
                if hasattr(o, attr) and getattr(o, attr) is not None:
                    try:
                        val = float(getattr(o, attr))
                        u += w * val
                    except Exception:
                        continue
            raw[oid] = u
        return raw

    def apply_attention_cost(self, raw_scores: Dict[str, float], outcome_set: List[Outcome]) -> Dict[str, float]:
        if not self.attention_attr:
            return raw_scores
        penalized = {}
        att_map = {o.id: float(getattr(o, self.attention_attr, 0.0)) for o in outcome_set}
        for oid, u in raw_scores.items():
            att_use = att_map.get(oid, 0.0)
            budget = self.attention_budget if self.attention_budget is not None else float("inf")
            exceed = max(0.0, att_use - budget)
            penalty = (att_use * self.attention_cost_coeff) + (exceed * self.attention_cost_coeff)
            penalized[oid] = u - penalty
        return penalized

    def normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        oids = list(scores.keys())
        vals = np.array([scores[k] for k in oids], dtype=float)
        if self.normalization_method == "minmax":
            mn, mx = vals.min(), vals.max()
            if abs(mx - mn) < self.eps:
                normed = np.full_like(vals, 0.5)
            else:
                normed = (vals - mn) / (mx - mn)
        elif self.normalization_method == "zscore":
            mu, sd = vals.mean(), vals.std()
            if sd < self.eps:
                normed = np.full_like(vals, 0.0)
            else:
                normed = (vals - mu) / sd
        else:
            raise ValueError("Unknown normalization method")
        return {oid: float(v) for oid, v in zip(oids, normed)}

    def to_probabilities(self, scores: Dict[str, float]) -> Dict[str, float]:
        oids = list(scores.keys())
        vals = np.array([scores[k] for k in oids], dtype=float)
        temp = max(self.eps, float(self.softmax_temp))
        shifted = vals - vals.max()
        exps = np.exp(shifted / temp)
        probs = exps / (exps.sum() + self.eps)
        return {oid: float(p) for oid, p in zip(oids, probs)}

    def choose_satisficing(self, normalized_scores: Dict[str, float]) -> Tuple[str, float]:
        if not normalized_scores:
            raise ValueError("No scores to choose from.")
        items = sorted(normalized_scores.items(), key=lambda kv: kv[1], reverse=True)
        if self.satisficing_threshold is not None:
            for oid, sc in items:
                if sc >= self.satisficing_threshold:
                    return oid, sc
        return items[0]

    def run(self, agent_preferences: Dict[str, float], outcome_set: List[Outcome], apply_attention: bool = True) -> Dict[str, Any]:
        raw = self.compute_raw(agent_preferences, outcome_set)
        penalized = self.apply_attention_cost(raw, outcome_set) if (apply_attention and self.attention_attr) else raw.copy()
        normalized = self.normalize_scores(penalized) if self.normalize else penalized
        probs = self.to_probabilities(penalized)
        chosen_id, chosen_score = self.choose_satisficing(normalized)
        return {
            "raw": raw,
            "penalized": penalized,
            "normalized": normalized,
            "probabilities": probs,
            "choice": {"id": chosen_id, "score": chosen_score}
        }

def compute_utility_service(request: ComputeUtilityRequest) -> ComputeUtilityResponse:
    utility_computer = ComputeUtility(
        normalize=request.normalize,
        normalization_method=request.normalization_method,
        attention_attr=request.attention_attr,
        attention_budget=request.attention_budget,
        attention_cost_coeff=request.attention_cost_coeff,
        softmax_temp=request.softmax_temp,
        satisficing_threshold=request.satisficing_threshold
    )

    result = utility_computer.run(
        agent_preferences=request.agent_preferences,
        outcome_set=request.outcome_set,
        apply_attention=request.apply_attention
    )

    print(f"Computed Utility: {result}")
    return ComputeUtilityResponse(
        raw=result["raw"],
        penalized=result["penalized"],
        normalized=result["normalized"],
        probabilities=result["probabilities"],
        choice=Choice(**result["choice"])
    )
