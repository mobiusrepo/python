from models.opportunity_cost_model import OpportunityCostRequest, OpportunityCostResponse
import numpy as np
import quantecon as qe
from typing import List, Dict, Any

class CognitiveAgent:
    def __init__(self):
        self.trade_off_profile: Dict[str, Dict[str, float]] = {}

    def expectedPayoffsMarkov(self, choice_set: List[str], payoff_matrix: Dict[str, float], P: np.ndarray) -> np.ndarray:
        n = len(choice_set)
        v = np.array([payoff_matrix.get(choice, 0.0) for choice in choice_set])
        mc = qe.MarkovChain(P)
        pi = np.array(mc.stationary_distributions[0]).flatten()

        if pi.size != n:
            pi = np.full(n, 1/n)

        expected_v = v * pi
        return expected_v

    def opportunityCost(self, choice_set: List[str], payoff_matrix: Dict[str, float], P: np.ndarray = None) -> Dict[str, Dict[str, float]]:
        n = len(choice_set)
        payoffs = self.expectedPayoffsMarkov(choice_set, payoff_matrix, P) if P is not None else np.array([payoff_matrix.get(choice, 0.0) for choice in choice_set])
        payoffs = np.array(payoffs).flatten()

        if payoffs.size != n:
            payoffs = np.full(n, payoffs[0] if payoffs.size == 1 else np.mean(payoffs))

        trade_off = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    trade_off[i, j] = payoffs[j] - payoffs[i]

        self.trade_off_profile = {
            choice_set[i]: {choice_set[j]: float(trade_off[i, j]) for j in range(n) if i != j}
            for i in range(n)
        }

        return self.trade_off_profile

def opportunity_cost_service(request: OpportunityCostRequest) -> OpportunityCostResponse:
    agent = CognitiveAgent()
    P_np = np.array(request.P) if request.P else None
    result = agent.opportunityCost(
        choice_set=request.choice_set,
        payoff_matrix=request.payoff_matrix,
        P=P_np
    )

    print(f"Opportunity Cost: {result}")
    return OpportunityCostResponse(trade_off_profile=result)
