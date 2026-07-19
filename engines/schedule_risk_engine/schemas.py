from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    task_id: str
    name: str
    start_date: str
    end_date: str
    float_days: int
    critical_path: bool

class RiskScore(BaseModel):
    task_id: str
    risk_level: str  # High, Medium, Low
    confidence: float
    factors: List[str]

class MitigationOption(BaseModel):
    description: str
    estimated_time_saved_days: int
    cost_impact: str

class MitigationPlan(BaseModel):
    task_id: str
    task_name: str
    risk_level: str
    confidence: float
    factors: List[str]
    mitigations: List[MitigationOption]
