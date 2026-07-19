from langchain_ollama import ChatOllama
from core.config import settings

def get_vlm(temperature: float = 0.1) -> ChatOllama:
    """
    Initializes a connection to the local Vision Language Model (VLM).
    We use llava:13b which is capable of processing base64 image data alongside text.
    """
    return ChatOllama(
        model="llava:13b",
        base_url=settings.ollama_base_url,
        temperature=temperature
    )
