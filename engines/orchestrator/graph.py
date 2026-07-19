from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from engines.orchestrator.state import AgentState
from engines.schedule_risk_engine.agent import analyze_schedule_risk
from engines.supply_chain_agent.agent import track_shipment_risk
from engines.rfi_intelligence_agent.agent import execute_rfi_query
from core.config import settings
import json

# Replace asyncpg with postgresql for standard sync connection pool
DB_URI = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
pool = ConnectionPool(conninfo=DB_URI, kwargs={"autocommit": True})

def schedule_node(state: AgentState):
    if state.get("schedule_tasks"):
        result = analyze_schedule_risk(state["schedule_tasks"])
        return {"risk_report": result}
    return {}

def supply_chain_node(state: AgentState):
    if state.get("shipments"):
        result = track_shipment_risk(state["shipments"])
        return {"supply_alerts": result}
    return {}

def rfi_node(state: AgentState):
    if state.get("rfi_query"):
        result = execute_rfi_query(state["rfi_query"])
        return {"rfi_answer": result}
    return {}

def human_interrupt_node(state: AgentState):
    # This node acts as a breakpoint. 
    # LangGraph natively handles interruption before nodes, but we can also use a dedicated node for explicit logic.
    return {"interrupt_reason": "Waiting for physical resolution."}

def router(state: AgentState):
    if state.get("interrupt_reason") and not state.get("human_resolution"):
        return "human_interrupt_node"
    return END

# Build Graph
builder = StateGraph(AgentState)
builder.add_node("schedule_node", schedule_node)
builder.add_node("supply_chain_node", supply_chain_node)
builder.add_node("rfi_node", rfi_node)
builder.add_node("human_interrupt_node", human_interrupt_node)

builder.set_entry_point("schedule_node")
builder.add_edge("schedule_node", "supply_chain_node")
builder.add_edge("supply_chain_node", "rfi_node")
builder.add_conditional_edges("rfi_node", router)
builder.add_edge("human_interrupt_node", END)

# Configure PostgreSQL Checkpointer
checkpointer = PostgresSaver(pool)
checkpointer.setup()

orchestrator_graph = builder.compile(checkpointer=checkpointer)
