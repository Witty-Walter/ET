from engines.spec_compliance.schemas import ComplianceReport
from engines.spec_compliance.extractor import extract_equipment_spec, compare_specs
from engines.spec_compliance.qa_evaluator import evaluate_narrative_compliance

def run_compliance_check(equipment_id: str, narrative_topic: str) -> ComplianceReport:
    """
    Runs the full Specification & Quality Compliance Engine.
    1. Extracts and compares hard numerical data.
    2. Evaluates qualitative narrative text using Bidirectional QA.
    """
    
    # 1. Hard Data Extraction & Comparison
    baseline_spec = extract_equipment_spec(f"Baseline design specs for {equipment_id}", equipment_id)
    submittal_spec = extract_equipment_spec(f"Contractor submittal specs for {equipment_id}", equipment_id)
    
    spec_deltas = compare_specs(baseline_spec, submittal_spec)
    
    # 2. Narrative QA Evaluation
    narrative_score = evaluate_narrative_compliance(narrative_topic)
    
    # 3. Compile Final Report
    is_compliant = True
    risk_reasons = []
    
    if any(delta.severity == "CRITICAL" for delta in spec_deltas):
        is_compliant = False
        risk_reasons.append("Critical hard data deviations found.")
        
    if narrative_score.score_pct < 90.0:
        is_compliant = False
        risk_reasons.append(f"Narrative compliance failed (Score: {narrative_score.score_pct}%).")
        
    risk_summary = " ".join(risk_reasons) if risk_reasons else "Submittal fully complies with baseline."
    
    return ComplianceReport(
        is_compliant=is_compliant,
        spec_deltas=spec_deltas,
        narrative_score=narrative_score,
        risk_summary=risk_summary
    )
