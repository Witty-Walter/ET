from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from engines.supply_chain_agent.schemas import Shipment
from engines.supply_chain_agent.agent import track_shipment_risk

router = APIRouter()

class SupplyChainAnalysisRequest(BaseModel):
    shipments: List[Shipment]

@router.post("/analyze")
async def analyze_supply_chain(request: SupplyChainAnalysisRequest) -> dict:
    """
    Analyzes active shipments and returns alerts for delayed or at-risk equipment.
    """
    try:
        result = track_shipment_risk(request.shipments)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
