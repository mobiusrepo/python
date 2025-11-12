from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    aggregate_weighted_choice_router,
    bounded_rationality_router,
    compute_utility_router,
    efficiency_ranking_router,
    incentive_alignment_router,
    opportunity_cost_router,
    payoff_weighted_aggregation_router,
    risk_assessment_router,
    scarcity_constraint_router,
)

app = FastAPI(title="Economics API",version = "1.0.0",root_path="/mobius-economic-science",root_path_in_servers=True)

# CORS Middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Economics API"}

app.include_router(aggregate_weighted_choice_router.router, prefix="/economics")
app.include_router(bounded_rationality_router.router, prefix="/economics")
app.include_router(compute_utility_router.router, prefix="/economics")
app.include_router(efficiency_ranking_router.router, prefix="/economics")
app.include_router(incentive_alignment_router.router, prefix="/economics")
app.include_router(opportunity_cost_router.router, prefix="/economics")
app.include_router(payoff_weighted_aggregation_router.router, prefix="/economics")
app.include_router(risk_assessment_router.router, prefix="/economics")
app.include_router(scarcity_constraint_router.router, prefix="/economics")
