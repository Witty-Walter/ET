import json
from langchain_core.messages import HumanMessage
from core.vlm_manager import get_vlm

def analyze_field_photo(photo_base64: str, pid_diagram_base64: str) -> dict:
    """
    Compares a real-world field photo against a digital P&ID diagram using a Vision Language Model.
    """
    vlm = get_vlm()
    
    # Langchain format for passing base64 images to multimodal models
    message = HumanMessage(
        content=[
            {
                "type": "text", 
                "text": "You are a Construction Commissioning Expert. Compare the first image (real-world field photo) to the second image (engineering P&ID diagram). Identify any discrepancies in piping, valve positions, or equipment orientation. Return your analysis strictly as a JSON object with keys: 'is_compliant' (boolean), 'discrepancies' (list of strings), and 'recommended_action' (string)."
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{photo_base64}"},
            },
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{pid_diagram_base64}"},
            },
        ]
    )
    
    try:
        response = vlm.invoke([message])
        # Parse the JSON response
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "is_compliant": False,
                "discrepancies": ["Failed to parse VLM response.", response.content],
                "recommended_action": "Manual review required."
            }
    except Exception as e:
        return {
            "is_compliant": False,
            "discrepancies": [f"VLM Error: {str(e)}"],
            "recommended_action": "Check VLM connection."
        }
