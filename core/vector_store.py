from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector
from core.config import settings

def get_vector_store(collection_name: str = "epc_langchain_embeddings") -> PGVector:
    """
    Initializes and returns a connection to the NeonDB pgvector store.
    """
    embeddings = OllamaEmbeddings(
        model=settings.ollama_embedding_model,
        base_url=settings.ollama_base_url
    )
    
    # PGVector requires psycopg (sync) for its internal operations,
    # so we replace asyncpg with psycopg in the connection string
    sync_db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
    
    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=sync_db_url,
        use_jsonb=True,
    )
    
    return vector_store
