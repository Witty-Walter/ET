from langchain_ollama import ChatOllama
from core.config import settings

def get_llm(temperature: float = 0.2):
    """
    Returns a configured ChatOllama instance using the globally defined model.
    """
    llm = ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=temperature,
    )
    return llm
