import httpx
import os

PROCORE_API_URL = "https://api.procore.com/rest/v1.0"
# In a production environment, this would be fetched dynamically via OAuth2
PROCORE_BEARER_TOKEN = os.getenv("PROCORE_TOKEN", "mock_token")
PROCORE_PROJECT_ID = os.getenv("PROCORE_PROJECT_ID", "12345")

async def push_defect_ticket(defect: dict) -> dict:
    """
    Pushes a defect identified by the AI as an Observation in Procore.
    """
    payload = {
        "project_id": PROCORE_PROJECT_ID,
        "observation_item": {
            "title": f"AI Field Defect: {defect.get('type', 'General')}",
            "description": "\n".join(defect.get("discrepancies", [])),
            "priority": "High" if defect.get("is_critical") else "Medium",
            "type_id": 1, # e.g. Quality
        }
    }
    
    headers = {
        "Authorization": f"Bearer {PROCORE_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Mocking the actual network request for the prototype
    if PROCORE_BEARER_TOKEN == "mock_token":
        return {"status": "mock_success", "procore_id": "OBS-9999", "payload": payload}
        
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PROCORE_API_URL}/observations/items", 
            json=payload, 
            headers=headers
        )
        response.raise_for_status()
        return response.json()
