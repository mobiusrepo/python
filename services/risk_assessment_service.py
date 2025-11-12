from models.risk_assessment_model import RiskAssessmentRequest, RiskAssessmentResponse, RiskMetrics
import numpy as np
from typing import Dict, List, Any
from scipy.stats import norm
import quantecon as qe

class RiskAgent:
    def __init__(self):
        self.risk_profile: Dict[str, RiskMetrics] = {}

    def riskAssessment(
        self,
        choice_set: List[str],
        payoff_matrix: Dict[str, float],
        prob_matrix: np.ndarray = None,
        confidence: float = 0.95
    ) -> Dict[str, RiskMetrics]:
        n = len(choice_set)
        payoffs = np.array([payoff_matrix.get(choice, 0.0) for choice in choice_set])

        if prob_matrix is not None:
            mc = qe.MarkovChain(prob_matrix)
            pi = np.array(mc.stationary_distributions[0]).flatten()
            if pi.size != n:
                pi = np.full(n, 1/n)  # uniform if mismatch
            expected_payoffs = payoffs * pi
        else:
            expected_payoffs = payoffs

        std_dev = np.std(expected_payoffs)
        z_score = norm.ppf(0.5 + confidence/2)
        ci = z_score * std_dev

        risk_adjusted = expected_payoffs - ci

        self.risk_profile = {
            choice_set[i]: RiskMetrics(
                ExpectedValue=float(expected_payoffs[i]),
                ConfidenceInterval=float(ci),
                RiskAdjustedValue=float(risk_adjusted[i])
            )
            for i in range(n)
        }

        return self.risk_profile

def risk_assessment_service(request: RiskAssessmentRequest) -> RiskAssessmentResponse:
    agent = RiskAgent()
    prob_matrix_np = np.array(request.prob_matrix) if request.prob_matrix else None
    result = agent.riskAssessment(
        choice_set=request.choice_set,
        payoff_matrix=request.payoff_matrix,
        prob_matrix=prob_matrix_np,
        confidence=request.confidence
    )

    print(f"Risk assessment: {result}")
    return RiskAssessmentResponse(risk_profile=result)
