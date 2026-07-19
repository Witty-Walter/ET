from fastapi import APIRouter, HTTPException, UploadFile, File
import base64
from pydantic import BaseModel
from engines.field_inspection.agent import analyze_field_photo
from core.pdf_utils import pdf_bytes_to_image_b64

router = APIRouter()

@router.post("/inspect")
async def inspect_field_photo(
    field_photo: UploadFile = File(...),
    pid_diagram: UploadFile = File(...)
) -> dict:
    """
    Analyzes a field photo against a P&ID diagram using a Vision Language Model.
    Supports both image files and PDF documents for the P&ID diagram.
    """
    try:
        # Read the field photo (must be an image)
        photo_bytes = await field_photo.read()
        photo_b64 = base64.b64encode(photo_bytes).decode('utf-8')
        
        # Read the P&ID diagram
        pid_bytes = await pid_diagram.read()
        
        # Check if PDF or image
        if pid_diagram.content_type == 'application/pdf' or pid_diagram.filename.lower().endswith('.pdf'):
            pid_b64 = pdf_bytes_to_image_b64(pid_bytes)
        else:
            pid_b64 = base64.b64encode(pid_bytes).decode('utf-8')
            
        result = analyze_field_photo(photo_b64, pid_b64)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
