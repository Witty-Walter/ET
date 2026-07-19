from fastapi import APIRouter, HTTPException, UploadFile, File
from core.pdf_utils import pdf_to_langchain_docs
from core.vector_store import get_vector_store

router = APIRouter()

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)) -> dict:
    """
    Accepts a PDF file, parses it with docling (layout-aware),
    and upserts the chunks into pgvector.
    """
    if not file.filename.lower().endswith('.pdf') and file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Only PDF files are supported for ingestion.")
        
    try:
        file_bytes = await file.read()
        
        # 1. Parse PDF to Langchain Documents using docling
        docs = pdf_to_langchain_docs(file_bytes, source_name=file.filename)
        
        if not docs:
            return {"chunks_ingested": 0, "source": file.filename, "message": "No content could be extracted."}
            
        # 2. Get Vector Store and add documents
        vector_store = get_vector_store()
        vector_store.add_documents(docs)
        
        return {
            "chunks_ingested": len(docs),
            "source": file.filename,
            "message": "Successfully ingested document into pgvector."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
