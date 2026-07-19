from fastapi import APIRouter, HTTPException
from engines.commissioning_agent.schemas import TestSubmission, EvaluationResult
from engines.commissioning_agent.agent import evaluate_test_submission

router = APIRouter()

@router.post("/evaluate-test", response_model=EvaluationResult)
async def evaluate_test(submission: TestSubmission) -> EvaluationResult:
    """
    Evaluates field test results against industry standards.
    """
    try:
        result = evaluate_test_submission(submission)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
