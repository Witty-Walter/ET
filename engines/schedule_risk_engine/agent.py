import os
import json
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from core.llm_manager import get_llm
from engines.schedule_risk_engine.schemas import Task, MitigationOption, MitigationPlan
from engines.schedule_risk_engine.tools.critical_path import calculate_cpm_risk

def analyze_schedule_risk(schedule_tasks: List[Task]) -> dict:
    """
    Analyzes project schedule for risk factors using CPM float calculations.
    Returns high and medium risk tasks along with LLM-generated mitigation plans.
    """
    risk_scores = calculate_cpm_risk(schedule_tasks)
    
    # Filter for high/medium risks
    at_risk_scores = [score for score in risk_scores if score.risk_level in ("HIGH", "MEDIUM")]
    at_risk_tasks = [score.dict() for score in at_risk_scores]
    
    # Initialize LLM and Prompt
    llm = get_llm(temperature=0.1)
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "mitigation_advisor.txt")
    with open(prompt_path, "r") as f:
        system_prompt = f.read()
        
    prompt = ChatPromptTemplate.from_template(system_prompt)
    
    # Create chain using JSON parser
    chain = prompt | llm | JsonOutputParser()
    
    mitigations = []
    
    for score in at_risk_scores:
        # find the corresponding task
        task = next(t for t in schedule_tasks if t.task_id == score.task_id)
        task_details = {
            "task_id": task.task_id,
            "task_name": task.name,
            "float_days": task.float_days,
            "critical_path": task.critical_path,
            "risk_factors": score.factors
        }
        
        try:
            # LLM invocation
            result = chain.invoke({
                "risk_level": score.risk_level,
                "task_details": json.dumps(task_details, indent=2)
            })
            
            # Ensure the result is a list
            if isinstance(result, dict):
                result = [result]
            elif not isinstance(result, list):
                result = []
                
            mitigation_options = [MitigationOption(**opt) for opt in result]
            
        except Exception as e:
            # Fallback mitigation if LLM fails
            error_msg = f"Error generating mitigations for {score.task_id}: {str(e)}"
            print(error_msg)
            mitigation_options = [
                MitigationOption(
                    description=error_msg,
                    estimated_time_saved_days=0,
                    cost_impact="Error"
                )
            ]
            
        plan = MitigationPlan(
            task_id=score.task_id,
            task_name=task.name,
            risk_level=score.risk_level,
            confidence=score.confidence,
            factors=score.factors,
            mitigations=mitigation_options
        )
        mitigations.append(plan.dict())
    
    return {
        "status": "analyzed",
        "total_tasks": len(schedule_tasks),
        "at_risk_count": len(at_risk_tasks),
        "at_risk_tasks": at_risk_tasks,
        "mitigations": mitigations
    }
