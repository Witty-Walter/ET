from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class TestSubmission(BaseModel):
    equipment_id: str = Field(..., description="The ID of the equipment being tested (e.g., GEN-01)")
    test_type: str = Field(..., description="The type of test being performed (e.g., Load Bank Test, Insulation Resistance)")
    recorded_values: Dict[str, Any] = Field(..., description="The empirical data recorded during the test (e.g., {'load_kw': 500, 'duration_mins': 120, 'temperature_c': 85})")
    notes: Optional[str] = Field(None, description="Any additional notes or observations from the field engineer")

class EvaluationResult(BaseModel):
    status: str = Field(..., description="The evaluation status: 'Pass', 'Fail', or 'Deviation'")
    cited_standard: str = Field(..., description="The specific standard or criteria document used for the evaluation (e.g., 'TIA-942 Section 5.1')")
    mitigation_recommendation: Optional[str] = Field(None, description="Actionable recommendation if the test failed or had a deviation")
    evaluation_summary: str = Field(..., description="A brief summary explaining the rationale behind the evaluation status")
