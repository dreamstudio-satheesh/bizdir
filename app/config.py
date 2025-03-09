from pydantic import BaseSettings
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

# Global settings instance
settings = Settings()

# Load the embedding model once to avoid redundant loads
embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
