from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from engines.schedule_risk_engine.schemas import Task
from engines.schedule_risk_engine.agent import analyze_schedule_risk

router = APIRouter()

class ScheduleAnalysisRequest(BaseModel):
    tasks: List[Task]

@router.post("/analyze")
async def analyze_schedule(request: ScheduleAnalysisRequest) -> dict:
    """
    Analyzes project schedule tasks and returns risk scores and mitigation plans.
    """
    try:
        result = analyze_schedule_risk(request.tasks)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
