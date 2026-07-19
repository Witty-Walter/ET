from core.vector_store import get_vector_store
from core.llm_manager import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

def two_stage_retrieve(query: str, k_initial: int = 20, k_final: int = 3) -> list[Document]:
    """
    Implements a robust two-stage retrieval pipeline.
    Stage 1: Fast Bi-Encoder search via PGVector to get top candidates.
    Stage 2: LLM Reranker (Zero-shot) to score and sort candidates precisely.
    """
    vector_store = get_vector_store()
    
    # Stage 1: Bi-Encoder (Ollama Embeddings via PGVector)
    try:
        candidates = vector_store.similarity_search(query, k=k_initial)
    except Exception:
        # Graceful degradation if vector store is empty during prototyping
        return []
        
    if not candidates:
        return []
        
    # Stage 2: LLM Zero-shot Reranker
    llm = get_llm(temperature=0.0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert retrieval judge. Score how relevant the document is to the query on a scale of 0 to 10. Only return the number, nothing else."),
        ("human", "Query: {query}\n\nDocument:\n{document}")
    ])
    
    chain = prompt | llm
    
    scored_candidates = []
    
    # We invoke the LLM for each candidate
    # In a true production app, this would be an async gather for speed
    for doc in candidates:
        try:
            result = chain.invoke({"query": query, "document": doc.page_content})
            score_str = result.content.strip()
            score = float(score_str)
        except ValueError:
            score = 0.0
            
        scored_candidates.append((score, doc))
        
    # Sort descending by score
    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    
    # Return top k_final documents
    return [doc for score, doc in scored_candidates[:k_final]]
