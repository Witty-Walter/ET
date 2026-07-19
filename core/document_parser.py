import uuid
from langchain_core.documents import Document

def parse_and_chunk_pdf(file_path: str) -> dict:
    """
    Parses a PDF using Docling for strictly local, highly accurate layout awareness.
    Returns a dictionary with 'parents' and 'children' lists of Langchain Documents.
    It separates tables from narrative text to allow accurate routing in the compliance engine.
    """
    # Import inside the function to avoid breaking initialization if docling isn't installed yet
    from docling.document_converter import DocumentConverter
    
    converter = DocumentConverter()
    result = converter.convert(file_path)
    docling_doc = result.document
    
    parents = []
    children = []
    
    current_parent_id = str(uuid.uuid4())
    current_parent_content = ""
    
    # 1. Extract Texts (Narrative)
    for text_item in docling_doc.texts:
        text_val = text_item.text
        
        # In a full implementation, we'd check text_item.label for 'title' vs 'paragraph'
        # For simplicity, we just chunk them sequentially under the current parent
        current_parent_content += "\n" + text_val
        
        children.append(Document(
            page_content=text_val,
            metadata={
                "parent_id": current_parent_id, 
                "type": "child", 
                "element_type": "text",
                "source": file_path
            }
        ))
        
        # If parent gets too big, cycle it
        if len(current_parent_content) > 1500:
            parents.append(Document(
                page_content=current_parent_content,
                metadata={"doc_id": current_parent_id, "type": "parent", "element_type": "text", "source": file_path}
            ))
            current_parent_id = str(uuid.uuid4())
            current_parent_content = ""
            
    # Finalize text parent
    if current_parent_content.strip():
        parents.append(Document(
            page_content=current_parent_content,
            metadata={"doc_id": current_parent_id, "type": "parent", "element_type": "text", "source": file_path}
        ))
        
    # 2. Extract Tables (Hard Data)
    for table_item in docling_doc.tables:
        table_md = table_item.export_to_markdown()
        
        table_parent_id = str(uuid.uuid4())
        
        parents.append(Document(
            page_content=table_md,
            metadata={"doc_id": table_parent_id, "type": "parent", "element_type": "table", "source": file_path}
        ))
        
        children.append(Document(
            page_content=table_md,
            metadata={"parent_id": table_parent_id, "type": "child", "element_type": "table", "source": file_path}
        ))

    return {"parents": parents, "children": children}
