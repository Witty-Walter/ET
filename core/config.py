from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    database_url: str
    redis_url: str
    
    ollama_model: str = "qwen3:8b"
    ollama_embedding_model: str = "nomic-embed-text"
    ollama_base_url: str = "http://localhost:11434"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
