from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

app = FastAPI(
    title="Data Centre EPC Project Intelligence Platform",
    description="AI-powered EPC Project Intelligence platform for data centre construction",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}

# Routers will be mounted here dynamically as we build out the engines
from api_gateway.routers import schedule_risk, supply_chain, rfi_intelligence, orchestrator, field_inspection, integrations, spec_compliance, document_ingestion, commissioning
app.include_router(spec_compliance.router, prefix="/api/v1/compliance", tags=["compliance"])
app.include_router(schedule_risk.router, prefix="/api/v1/schedule", tags=["schedule"])
app.include_router(supply_chain.router, prefix="/api/v1/supply-chain", tags=["supply-chain"])
app.include_router(field_inspection.router, prefix="/api/v1/field", tags=["field-inspection"])
app.include_router(rfi_intelligence.router, prefix="/api/v1/rfi", tags=["rfi"])
app.include_router(orchestrator.router, prefix="/api/v1/orchestrate", tags=["orchestrator"])
app.include_router(integrations.router, prefix="/api/v1/integrations", tags=["integrations"])
app.include_router(document_ingestion.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(commissioning.router, prefix="/api/v1/commissioning", tags=["commissioning"])

