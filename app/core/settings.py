from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    HOST: str
    PORT: int

    DEBUG: bool

    
    GROQ_API_KEY: str = ""
    

    NEO4J_URI: str = ""
    NEO4J_USERNAME: str = ""
    NEO4J_PASSWORD: str = ""
    EMBEDDING_MODEL:str = ""
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    GEMINI_API_KEY:str
    COHERE_API_KEY:str
    GEMINI_MODEL:str
    COHERE_MODEL:str
    LLM_PROVIDER:str
    DATABASE_URL: str
    COHERE_EMBEDDING_MODEL:str
    JWT_SECRET:str
    JWT_ALGORITHM:str="HS256"
    JWT_EXPIRE_MINUTES:int=60

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()