from pydantic import BaseModel, Field
from typing import Optional, List

class EquipmentSpec(BaseModel):
    equipment_id: str = Field(description="Unique identifier for the equipment (e.g. Pump-01)")
    voltage_v: Optional[float] = Field(None, description="Operating voltage in Volts")
    current_a: Optional[float] = Field(None, description="Operating current in Amperes")
    power_kw: Optional[float] = Field(None, description="Power requirement in Kilowatts")
    dimensions_mm: Optional[List[float]] = Field(None, description="Physical dimensions in mm (L, W, H)")
    weight_kg: Optional[float] = Field(None, description="Weight in kilograms")
    temperature_rating_c: Optional[float] = Field(None, description="Maximum operating temperature in Celsius")

class SpecDelta(BaseModel):
    field: str
    baseline_value: Optional[float | List[float]]
    submittal_value: Optional[float | List[float]]
    delta: Optional[float | List[float]]
    severity: str

class ComplianceScore(BaseModel):
    score_pct: float
    questions: List[str]
    answers: List[str]
    reasoning: str

class ComplianceReport(BaseModel):
    is_compliant: bool
    spec_deltas: List[SpecDelta]
    narrative_score: ComplianceScore
    risk_summary: str
