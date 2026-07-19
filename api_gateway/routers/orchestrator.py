from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from engines.orchestrator.graph import orchestrator_graph
from engines.orchestrator.state import AgentState
from engines.schedule_risk_engine.schemas import Task
from engines.supply_chain_agent.schemas import Shipment
from engines.rfi_intelligence_agent.schemas import RFIQuery

router = APIRouter()

class OrchestratorRequest(BaseModel):
    session_id: str
    schedule_tasks: Optional[List[Task]] = None
    shipments: Optional[List[Shipment]] = None
    rfi_query: Optional[RFIQuery] = None

class ResumeRequest(BaseModel):
    session_id: str
    human_resolution: str

@router.post("/run")
async def run_orchestrator(request: OrchestratorRequest):
    """
    Starts or updates a LangGraph orchestration run.
    """
    try:
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Prepare the state payload
        state_payload = {
            "session_id": request.session_id,
            "schedule_tasks": request.schedule_tasks,
            "shipments": request.shipments,
            "rfi_query": request.rfi_query,
            "defects": [],
            "interrupt_reason": None,
            "human_resolution": None
        }
        
        # Stream the graph execution until it hits an interrupt or END
        final_state = None
        for chunk in orchestrator_graph.stream(state_payload, config):
            final_state = chunk
            
        return {"status": "success", "state": final_state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/resume")
async def resume_orchestrator(request: ResumeRequest):
    """
    Resumes a paused LangGraph orchestration run after a human-in-the-loop interrupt.
    """
    try:
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Provide the human resolution to the state to unblock the router
        state_payload = {
            "human_resolution": request.human_resolution,
            "interrupt_reason": None # Clear the interrupt
        }
        
        orchestrator_graph.update_state(config, state_payload)
        
        # Resume graph
        final_state = None
        for chunk in orchestrator_graph.stream(None, config):
            final_state = chunk
            
        return {"status": "resumed", "state": final_state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
