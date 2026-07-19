import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from core.llm_manager import get_llm
from core.vector_store import get_vector_store
from engines.rfi_intelligence_agent.schemas import RFIQuery, ChatResponse, Citation

def get_rfi_agent():
    """
    Initializes the RAG chain for the RFI Intelligence Agent.
    """
    llm = get_llm(temperature=0.1)
    
    prompt_path = os.path.join(os.path.dirname(__file__), "prompts", "rag_system.txt")
    with open(prompt_path, "r") as f:
        system_prompt = f.read()
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}")
    ])
    
    def format_docs(docs):
        return "\n\n".join(
            f"[Document Name: {doc.metadata.get('source', 'Unknown')}]\n{doc.page_content}" 
            for doc in docs
        )
        
    rag_chain = (
        {"context": RunnablePassthrough() | format_docs, "query": RunnablePassthrough()}
        | prompt
        | llm
    )
    
    return rag_chain

def fetch_parent_documents(query: str, k: int = 5):
    """
    Implements Layout-Aware RAG (LARAG):
    1. Searches for specific child chunks (tables, lists, text)
    2. Retrieves their full parent chunk (Title + body context)
    """
    vector_store = get_vector_store()
    
    # In a real implementation we would use filters `filter={"type": "child"}` 
    # but to support an empty/mock DB gracefully without crashing pgvector filters:
    try:
        child_docs = vector_store.similarity_search(query, k=k)
    except Exception:
        return []
        
    # Mocking the parent retrieval for the prototype to avoid complex PGVector JSONB filters
    # If the docs have a parent_id, we would fetch that. Here we just return the docs themselves
    # as "parents" if we don't have full LARAG data populated yet.
    return child_docs

def execute_rfi_query(rfi_query: RFIQuery) -> ChatResponse:
    """
    Executes a query against the RAG chain using Layout-Aware parent documents.
    """
    rag_chain = get_rfi_agent()
    
    # 1. Fetch LARAG documents
    parent_docs = fetch_parent_documents(rfi_query.query)
    
    citations = []
    for doc in parent_docs:
        citations.append(Citation(
            document_id=str(doc.metadata.get('doc_id', 'unknown')),
            source=doc.metadata.get('source', 'Unknown'),
            page_number=doc.metadata.get('page', None),
            excerpt=doc.page_content[:300]
        ))
        
    # 2. Invoke the chain passing the full parent docs as context
    llm_response = rag_chain.invoke(parent_docs)
    
    return ChatResponse(
        answer=llm_response.content,
        citations=citations
    )
