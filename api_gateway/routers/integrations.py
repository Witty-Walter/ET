from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from integrations.procore import push_defect_ticket
from integrations.handover_compiler import compile_handover_manual

router = APIRouter()

class DefectRequest(BaseModel):
    type: str
    is_critical: bool
    discrepancies: list[str]

@router.post("/procore/defect")
async def create_procore_defect(defect: DefectRequest):
    """
    Pushes a defect to Procore.
    """
    try:
        result = await push_defect_ticket(defect.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/handover/{project_id}")
async def get_handover_manual(project_id: str):
    """
    Compiles and downloads the O&M Handover Manual PDF.
    """
    try:
        pdf_bytes = compile_handover_manual(project_id)
        # If typst isn't installed it returns the raw source code, so we set content type accordingly
        is_pdf = pdf_bytes.startswith(b"%PDF")
        media_type = "application/pdf" if is_pdf else "text/plain"
        return Response(content=pdf_bytes, media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
