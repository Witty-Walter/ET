import base64
import fitz  # PyMuPDF
from io import BytesIO
from langchain_core.documents import Document
from docling.document_converter import DocumentConverter

def pdf_bytes_to_image_b64(pdf_bytes: bytes, page_index: int = 0, dpi: int = 200) -> str:
    """
    Takes PDF bytes, renders the specified page at `dpi` resolution using pymupdf,
    and returns a Base64-encoded JPEG/PNG string.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    if page_index >= len(doc):
        page_index = len(doc) - 1
        
    page = doc.load_page(page_index)
    pix = page.get_pixmap(dpi=dpi)
    
    # Return base64 encoded PNG
    img_bytes = pix.tobytes("png")
    return base64.b64encode(img_bytes).decode("utf-8")

def pdf_b64_to_image_b64(pdf_b64: str, page_index: int = 0, dpi: int = 200) -> str:
    """
    Takes a Base64-encoded PDF string, decodes it, and renders to an image Base64.
    """
    # Strip any prefix like "data:application/pdf;base64," if present
    if "base64," in pdf_b64:
        pdf_b64 = pdf_b64.split("base64,")[1]
    
    pdf_bytes = base64.b64decode(pdf_b64)
    return pdf_bytes_to_image_b64(pdf_bytes, page_index, dpi)

def pdf_to_langchain_docs(file_bytes: bytes, source_name: str) -> list[Document]:
    """
    Uses docling to parse a PDF into a list of LangChain Document objects.
    """
    # Write to a temporary file since docling might require a file path
    # For now, if docling allows DocumentConverter.convert(stream), use it.
    import tempfile
    import os
    
    docs = []
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
        
    try:
        converter = DocumentConverter()
        result = converter.convert(tmp_path)
        
        # docling outputs a Document object which can be exported to markdown
        # or we can iterate over texts/tables. 
        # For simplicity, we can just export the whole document to markdown and chunk it,
        # or use its layout chunks.
        
        # Exporting to markdown for a simple layout-aware representation:
        md_content = result.document.export_to_markdown()
        
        # We can split the markdown by headers for simple layout-aware chunking
        # Or just store the whole document text if small enough.
        # Let's chunk it roughly by paragraphs/sections here, or just return one large chunk 
        # and let standard splitters handle it later if needed.
        # For this implementation, we return the entire markdown as one Document
        
        doc = Document(
            page_content=md_content,
            metadata={"source": source_name, "type": "pdf"}
        )
        docs.append(doc)
    finally:
        os.unlink(tmp_path)
        
    return docs
