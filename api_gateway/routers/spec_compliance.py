from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from engines.spec_compliance.schemas import ComplianceReport
from engines.spec_compliance.agent import run_compliance_check

router = APIRouter()

class ComplianceRequest(BaseModel):
    equipment_id: str
    narrative_topic: str

@router.post("/compare")
async def compare_specifications(request: ComplianceRequest) -> ComplianceReport:
    """
    Compares Baseline Specs against Contractor Submittals using:
    - JSON Hard Data Extraction
    - Bidirectional QA (QuestEval)
    """
    try:
        result = run_compliance_check(request.equipment_id, request.narrative_topic)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
