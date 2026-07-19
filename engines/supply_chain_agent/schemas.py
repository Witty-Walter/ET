from pydantic import BaseModel
from typing import List, Optional

class SupplierRisk(BaseModel):
    supplier_id: str
    name: str
    historical_delay_probability: float

class Shipment(BaseModel):
    tracking_number: str
    equipment_type: str
    origin: str
    destination: str
    status: str
    estimated_arrival: str
    at_risk: bool

class ProcurementAlert(BaseModel):
    alert_type: str
    severity: str
    message: str
    affected_shipments: List[Shipment]
