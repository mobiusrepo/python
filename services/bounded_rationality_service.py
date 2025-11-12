from models.bounded_rationality_model import BoundedRationalityRequest, BoundedRationalityResponse
import numpy as np
import random
from typing import List, Dict, Any, Tuple, Optional

try:
    from ax.service.managed_loop import optimize as ax_optimize
    AX_AVAILABLE = True
except Exception:
    AX_AVAILABLE = False

class BoundedAgent:
    def __init__(self):
        self.simplified_choice: Optional[str] = None
        self.heuristic_trace: List[Dict[str, Any]] = []

    def boundedRationality(
        self,
        choice_set: List[str],
        payoff_matrix: Dict[str, float],
        agent_capacity: Dict[str, float],
        decision_tree: Optional[Dict[str, Any]] = None,
        mode: str = "satisficing",
        aspiration: Optional[float] = None,
        sample_budget: int = 5,
        random_seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        rng = np.random.RandomState(random_seed)
        max_evals = int(agent_capacity.get("max_evals", sample_budget))
        budget = min(max_evals, sample_budget)

        payoffs_arr = np.array([payoff_matrix.get(c, 0.0) for c in choice_set])
        if aspiration is None:
            aspiration = float(np.median(payoffs_arr))

        trace: List[Dict[str, Any]] = []

        def record(choice: str, payoff: float, rank: int, note: str = ""):
            trace.append({
                "choice": choice,
                "payoff": float(payoff),
                "evaluated_at_rank": int(rank),
                "note": note
            })

        if mode == "satisficing":
            order = []
            if decision_tree and isinstance(decision_tree.get("order"), list):
                order = [c for c in decision_tree["order"] if c in choice_set]
                order += [c for c in choice_set if c not in order]
            else:
                order = sorted(choice_set, key=lambda c: payoff_matrix.get(c, 0.0), reverse=True)

            selected = None
            eval_count = 0
            for rank, choice in enumerate(order):
                if eval_count >= budget:
                    break
                pf = payoff_matrix.get(choice, 0.0)
                note = "meets aspiration" if pf >= aspiration else "below aspiration"
                record(choice, pf, rank + 1, note)
                eval_count += 1
                if pf >= aspiration:
                    selected = choice
                    break

            if selected is None:
                if len(trace) > 0:
                    best = max(trace, key=lambda r: r["payoff"])
                    selected = best["choice"]
                    for t in trace:
                        if t["choice"] == selected:
                            t["note"] += " | chosen (best evaluated)"
                else:
                    selected = max(choice_set, key=lambda c: payoff_matrix.get(c, 0.0))
                    record(selected, payoff_matrix.get(selected, 0.0), 0, "chosen (fallback)")

            self.simplified_choice = selected
            self.heuristic_trace = trace
            return {"SimplifiedChoice": selected, "HeuristicTrace": trace}

        elif mode == "simulate":
            candidates = list(choice_set)
            rng.shuffle(candidates)
            candidates = candidates[:budget]
            for rank, choice in enumerate(candidates):
                pf = payoff_matrix.get(choice, 0.0)
                record(choice, pf, rank + 1, "simulated evaluation")
            best = max(trace, key=lambda r: r["payoff"])
            selected = best["choice"]
            for t in trace:
                if t["choice"] == selected:
                    t["note"] += " | chosen"
            self.simplified_choice = selected
            self.heuristic_trace = trace
            return {"SimplifiedChoice": selected, "HeuristicTrace": trace}

        elif mode == "bayes":
            if not AX_AVAILABLE:
                return self.boundedRationality(choice_set, payoff_matrix, agent_capacity, decision_tree,
                                              mode="simulate", aspiration=aspiration,
                                              sample_budget=sample_budget, random_seed=random_seed)
            domain = [{"name": "choice", "type": "choice", "values": choice_set}]
            def evaluation_func(params):
                choice = params["choice"]
                return {"payoff": float(payoff_matrix.get(choice, 0.0))}

            trials = min(budget, max(1, int(agent_capacity.get("max_evals", sample_budget))))
            best = None
            best_val = -np.inf
            try:
                best_parameters, values, experiment, model = ax_optimize(
                    parameters=domain,
                    evaluation_function=evaluation_func,
                    total_trials=trials,
                )
                best_choice = best_parameters["choice"]
                selected = best_choice
                for i, c in enumerate(choice_set[:trials]):
                    record(c, payoff_matrix.get(c, 0.0), i + 1, "bayes-trial (approx)")
                for t in trace:
                    if t["choice"] == selected:
                        t["note"] += " | chosen"
                self.simplified_choice = selected
                self.heuristic_trace = trace
                return {"SimplifiedChoice": selected, "HeuristicTrace": trace}
            except Exception:
                return self.boundedRationality(choice_set, payoff_matrix, agent_capacity, decision_tree,
                                              mode="simulate", aspiration=aspiration,
                                              sample_budget=sample_budget, random_seed=random_seed)

        else:
            raise ValueError("Unknown mode. Use 'satisficing', 'simulate', or 'bayes'.")

def bounded_rationality_service(request: BoundedRationalityRequest) -> BoundedRationalityResponse:
    agent = BoundedAgent()
    result = agent.boundedRationality(
        choice_set=request.choice_set,
        payoff_matrix=request.payoff_matrix,
        agent_capacity=request.agent_capacity,
        decision_tree=request.decision_tree,
        mode=request.mode,
        aspiration=request.aspiration,
        sample_budget=request.sample_budget,
        random_seed=request.random_seed
    )

    print(f"Bounded Rationality: {result}")
    return BoundedRationalityResponse(
        simplified_choice=result["SimplifiedChoice"],
        heuristic_trace=result["HeuristicTrace"]
    )
