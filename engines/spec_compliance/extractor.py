from core.retriever import two_stage_retrieve
from core.llm_manager import get_llm
from engines.spec_compliance.schemas import EquipmentSpec, SpecDelta

def extract_equipment_spec(query: str, equipment_id: str) -> EquipmentSpec:
    """
    Extracts hard numeric data from the document into a strict JSON schema using the Two-Stage Retriever.
    """
    # 1. Retrieve the most relevant chunks (e.g. Docling parsed tables)
    relevant_docs = two_stage_retrieve(query, k_initial=10, k_final=2)
    
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    # 2. Extract structured data
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(EquipmentSpec)
    
    prompt = f"""
    You are an expert engineer extracting technical specifications.
    Extract the specifications for equipment ID '{equipment_id}' from the following context.
    If a value is not found, leave it as null.
    
    Context:
    {context}
    """
    
    result = structured_llm.invoke(prompt)
    return result

def compare_specs(baseline: EquipmentSpec, submittal: EquipmentSpec) -> list[SpecDelta]:
    """
    Deterministically compares two extracted EquipmentSpecs (No AI used here).
    """
    deltas = []
    
    fields_to_check = ["voltage_v", "current_a", "power_kw", "weight_kg", "temperature_rating_c"]
    
    for field in fields_to_check:
        base_val = getattr(baseline, field)
        sub_val = getattr(submittal, field)
        
        if base_val is not None and sub_val is not None:
            diff = abs(base_val - sub_val)
            # If there's a difference > 0, it's a deviation
            severity = "CRITICAL" if diff > 0 else "PASS"
            if diff > 0:
                deltas.append(SpecDelta(
                    field=field,
                    baseline_value=base_val,
                    submittal_value=sub_val,
                    delta=diff,
                    severity=severity
                ))
                
    # Dimensions (List of floats)
    if baseline.dimensions_mm and submittal.dimensions_mm:
        if len(baseline.dimensions_mm) == len(submittal.dimensions_mm):
            dims_diff = [abs(b - s) for b, s in zip(baseline.dimensions_mm, submittal.dimensions_mm)]
            if any(d > 0 for d in dims_diff):
                deltas.append(SpecDelta(
                    field="dimensions_mm",
                    baseline_value=baseline.dimensions_mm,
                    submittal_value=submittal.dimensions_mm,
                    delta=dims_diff,
                    severity="CRITICAL"
                ))
                
    return deltas
