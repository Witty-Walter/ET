from typing import TypedDict, List, Optional, Any
from engines.schedule_risk_engine.schemas import Task, MitigationPlan
from engines.supply_chain_agent.schemas import Shipment, ProcurementAlert
from engines.rfi_intelligence_agent.schemas import RFIQuery, ChatResponse

class AgentState(TypedDict):
    session_id: str
    
    # Inputs
    schedule_tasks: Optional[List[Task]]
    shipments: Optional[List[Shipment]]
    rfi_query: Optional[RFIQuery]
    
    # Outputs
    risk_report: Optional[dict]
    supply_alerts: Optional[dict]
    rfi_answer: Optional[ChatResponse]
    
    # Orchestrator tracking
    defects: List[dict]
    interrupt_reason: Optional[str]
    human_resolution: Optional[str]
