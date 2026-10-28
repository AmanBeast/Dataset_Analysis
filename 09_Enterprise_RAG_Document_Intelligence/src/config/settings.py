"""
Application Configuration Module.

Centralizes system settings, environment variables, default model choices,
chunking parameters, and logging setup following Clean Architecture guidelines.
"""

import os
import logging
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass(frozen=True)
class Settings:
    """Immutable Application Settings."""

    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Embedding Model Settings
    EMBEDDING_MODEL_NAME: str = os.getenv(
        "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
    )

    # LLM Settings
    GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))

    # Document Chunking Settings
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "150"))

    # Vector Retriever Settings
    RETRIEVER_K: int = int(os.getenv("RETRIEVER_K", "4"))
    RETRIEVAL_STRATEGY: str = os.getenv("RETRIEVAL_STRATEGY", "similarity")  # similarity or mmr

    # Paths & Caching
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    CACHE_DIR: Path = BASE_DIR / os.getenv("CACHE_DIR", ".faiss_cache")
    TEMP_DIR: Path = BASE_DIR / "temp_uploads"

    def validate() -> None:
        """Ensure necessary directories exist."""
        os.makedirs(Settings.CACHE_DIR, exist_ok=True)
        os.makedirs(Settings.TEMP_DIR, exist_ok=True)

# Run validation on import
Settings.validate()

# Configure Application-wide Logger
def setup_logger(name: str = "DocumentIntelligence") -> logging.Logger:
    """Creates and configures a standardized logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger

logger = setup_logger()
