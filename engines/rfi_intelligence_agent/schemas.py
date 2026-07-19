from pydantic import BaseModel, Field
from typing import List, Optional

class Citation(BaseModel):
    document_id: str
    source: str
    page_number: Optional[int]
    excerpt: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation] = Field(default_factory=list)

class RFIQuery(BaseModel):
    query: str
    session_id: str
