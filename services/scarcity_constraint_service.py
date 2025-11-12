from models.scarcity_constraint_model import ScarcityConstraintRequest, ScarcityConstraintResponse
import cvxpy as cp
from typing import Dict, Any, List

class ScarcityConstraintCVXPY:
    def __init__(self):
        self.constraint_set: Dict[str, bool] = {}
        self.feasibility_map: Dict[str, float] = {}
        self.infeasible_options: List[str] = []
        self.binding_constraints: Dict[str, List[str]] = {}

    def scarcityConstraint(
        self,
        resource_pool: Dict[str, float],
        demand_vector: Dict[str, Dict[str, float]]
    ) -> Dict[str, Any]:
        self.constraint_set = {}
        self.feasibility_map = {}
        self.infeasible_options = []
        self.binding_constraints = {}

        for option, demands in demand_vector.items():
            scale = cp.Variable()

            constraints = []
            for resource, available in resource_pool.items():
                required = demands.get(resource, 0)
                constraints.append(scale * required <= available)

            constraints.append(scale >= 0)
            constraints.append(scale <= 1)

            problem = cp.Problem(cp.Maximize(scale), constraints)
            problem.solve(solver=cp.SCS)

            scale_value = scale.value if scale.value is not None else 0.0

            feasible = bool(scale_value >= 1.0 - 1e-6)
            self.feasibility_map[option] = float(scale_value)
            self.constraint_set[option] = feasible

            if not feasible:
                self.infeasible_options.append(option)

                self.binding_constraints[option] = []
                for resource, available in resource_pool.items():
                    required = demands.get(resource, 0)
                    if required > 0:
                        max_scale = available / required
                        if max_scale < 1.0 + 1e-6:
                            self.binding_constraints[option].append(resource)

        return {
            "ConstraintSet": self.constraint_set,
            "FeasibilityMap": self.feasibility_map,
            "InfeasibleOptions": self.infeasible_options,
            "BindingConstraints": self.binding_constraints
        }

def scarcity_constraint_service(request: ScarcityConstraintRequest) -> ScarcityConstraintResponse:
    agent = ScarcityConstraintCVXPY()
    result = agent.scarcityConstraint(
        resource_pool=request.resource_pool,
        demand_vector=request.demand_vector
    )

    print(f"Scarcity constraint check: {result}")
    return ScarcityConstraintResponse(
        constraint_set=result["ConstraintSet"],
        feasibility_map=result["FeasibilityMap"],
        infeasible_options=result["InfeasibleOptions"],
        binding_constraints=result["BindingConstraints"]
    )
