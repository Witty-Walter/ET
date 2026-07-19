from typing import List
from engines.supply_chain_agent.schemas import ProcurementAlert, Shipment

def track_shipment_risk(active_shipments: List[Shipment]) -> dict:
    """
    Analyzes active shipments and generates alerts for any delayed or at-risk equipment.
    """
    at_risk = [s for s in active_shipments if s.at_risk]
    alerts = []
    
    if at_risk:
        alert = ProcurementAlert(
            alert_type="SUPPLY_CHAIN_DELAY",
            severity="HIGH",
            message=f"{len(at_risk)} critical equipment shipments are currently at risk of delay.",
            affected_shipments=at_risk
        )
        alerts.append(alert.dict())
        
    return {
        "status": "tracked",
        "total_shipments_tracked": len(active_shipments),
        "alerts_generated": len(alerts),
        "alerts": alerts
    }
