from typing import List
from engines.schedule_risk_engine.schemas import Task, RiskScore

def calculate_cpm_risk(tasks: List[Task]) -> List[RiskScore]:
    """
    Evaluates risk based on critical path method (CPM) heuristics.
    Tasks with float_days == 0 are on the critical path and are automatically HIGH risk.
    Tasks with float_days <= 3 are MEDIUM risk.
    """
    risk_scores = []
    
    for task in tasks:
        if task.float_days == 0 or task.critical_path:
            risk = RiskScore(
                task_id=task.task_id,
                risk_level="HIGH",
                confidence=0.95,
                factors=["Zero float (Critical Path)", "Immediate delay impact"]
            )
        elif task.float_days <= 3:
            risk = RiskScore(
                task_id=task.task_id,
                risk_level="MEDIUM",
                confidence=0.80,
                factors=["Low float (Near Critical)", "Minimal buffer"]
            )
        else:
            risk = RiskScore(
                task_id=task.task_id,
                risk_level="LOW",
                confidence=0.90,
                factors=[f"Adequate float buffer ({task.float_days} days)"]
            )
            
        risk_scores.append(risk)
        
    return risk_scores
