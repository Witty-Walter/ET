from fastapi import APIRouter, HTTPException
from engines.rfi_intelligence_agent.schemas import RFIQuery, ChatResponse
from engines.rfi_intelligence_agent.agent import execute_rfi_query

router = APIRouter()

@router.post("/query")
async def query_rfi(request: RFIQuery) -> ChatResponse:
    """
    Submits a query to the RFI Intelligence Agent and returns the answer with citations.
    """
    try:
        response = execute_rfi_query(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
