import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from core.llm_manager import get_llm
from core.vector_store import get_vector_store
from engines.commissioning_agent.schemas import TestSubmission, EvaluationResult

def get_commissioning_agent():
    """
    Initializes the RAG chain for the Commissioning Quality Assurance Copilot.
    Uses structured output to guarantee the EvaluationResult schema.
    """
    # Use a low temperature for evaluation/QA tasks
    llm = get_llm(temperature=0.0)
    structured_llm = llm.with_structured_output(EvaluationResult)
    
    system_prompt = (
        "You are an expert Data Centre Commissioning Engineer and QA Auditor. "
        "Your job is to evaluate field test results against industry standards (e.g., TIA-942, BICSI, Uptime Institute). "
        "Review the provided testing standards context, and evaluate the field engineer's recorded values. "
        "Determine if the test passes, fails, or has a deviation. "
        "Provide a specific citation to the standard, a brief summary of the evaluation, and any recommended mitigation if the test did not pass.\n\n"
        "Context Standards:\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Test Submission Details:\nEquipment ID: {equipment_id}\nTest Type: {test_type}\nRecorded Values: {recorded_values}\nNotes: {notes}")
    ])
    
    def format_docs(docs):
        if not docs:
            return "No specific standards found in the database for this test type. Please evaluate based on general engineering best practices."
        return "\n\n".join(
            f"[Source: {doc.metadata.get('source', 'Unknown Document')}]\n{doc.page_content}" 
            for doc in docs
        )
        
    rag_chain = (
        {
            "context": lambda x: format_docs(x["docs"]), 
            "equipment_id": lambda x: x["submission"].equipment_id,
            "test_type": lambda x: x["submission"].test_type,
            "recorded_values": lambda x: json.dumps(x["submission"].recorded_values),
            "notes": lambda x: x["submission"].notes or "None"
        }
        | prompt
        | structured_llm
    )
    
    return rag_chain

def evaluate_test_submission(submission: TestSubmission) -> EvaluationResult:
    """
    Executes the commissioning evaluation RAG chain for a given test submission.
    """
    # Initialize vector store for the specific collection
    vector_store = get_vector_store(collection_name="commissioning_standards")
    
    # We use a try-except block here to handle the case where the pgvector table 
    # might not exist yet or is completely empty, preventing similarity search errors.
    try:
        # Search for standards related to the test type
        docs = vector_store.similarity_search(submission.test_type, k=3)
    except Exception:
        docs = []
        
    rag_chain = get_commissioning_agent()
    
    # Pass the retrieved documents and the submission data to the chain
    result = rag_chain.invoke({
        "submission": submission,
        "docs": docs # Docs are passed into the chain, we need to adjust RunnablePassthrough
    })
    
    return result
