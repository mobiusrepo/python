from models.incentive_alignment_model import IncentiveAlignmentRequest, IncentiveAlignmentResponse
import numpy as np
import cvxpy as cp
from typing import List, Dict, Any

class IncentiveAgent:
    def __init__(self):
        self.updated_strategy: Dict[str, float] = {}
        self.expected_payoff: float = 0.0

    def incentiveAlignment(
        self,
        choice_set: List[str],
        payoff_matrix: Dict[str, float],
        global_target: float = None,
        epsilon: float = 1e-3
    ) -> Dict[str, Any]:
        n = len(choice_set)
        x = cp.Variable(n)  # decision variables for each choice
        payoffs = np.array([payoff_matrix.get(c, 0.0) for c in choice_set])

        objective = cp.Maximize(payoffs @ x)

        constraints = [
            x >= 0,
            cp.sum(x) == 1
        ]

        if global_target is not None:
            constraints.append(payoffs @ x >= global_target - epsilon)

        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.SCS)

        raw_strategy = np.array([float(x.value[i]) for i in range(n)])
        raw_strategy = np.clip(raw_strategy, 0.0, None)
        if raw_strategy.sum() > 0:
            normalized_strategy = raw_strategy / raw_strategy.sum()
        else:
            normalized_strategy = np.ones(n) / n

        expected_payoff = float(payoffs @ normalized_strategy)

        self.updated_strategy = {choice_set[i]: float(normalized_strategy[i]) for i in range(n)}
        self.expected_payoff = expected_payoff

        return {
            "UpdatedStrategy": self.updated_strategy,
            "ExpectedPayoff": self.expected_payoff,
            "TargetSatisfied": global_target is None or expected_payoff >= global_target - epsilon
        }

def incentive_alignment_service(request: IncentiveAlignmentRequest) -> IncentiveAlignmentResponse:
    agent = IncentiveAgent()
    result = agent.incentiveAlignment(
        choice_set=request.choice_set,
        payoff_matrix=request.payoff_matrix,
        global_target=request.global_target,
        epsilon=request.epsilon
    )

    print(f"Incentive Alignment: {result}")
    return IncentiveAlignmentResponse(
        updated_strategy=result["UpdatedStrategy"],
        expected_payoff=result["ExpectedPayoff"],
        target_satisfied=result["TargetSatisfied"]
    )
