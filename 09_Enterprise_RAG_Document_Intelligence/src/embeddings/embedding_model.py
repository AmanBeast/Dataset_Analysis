"""
HuggingFace Embedding Model Manager.

Encapsulates HuggingFace embeddings instantiation with singleton caching.
"""

from typing import Optional
from langchain_core.embeddings import Embeddings
from config.settings import Settings, logger
from core.exceptions import EmbeddingError

class EmbeddingModelFactory:
    """Factory and manager for HuggingFace embeddings."""

    _instance: Optional[Embeddings] = None

    @classmethod
    def get_embedding_model(cls, model_name: Optional[str] = None) -> Embeddings:
        """
        Retrieves cached HuggingFaceEmbeddings instance or creates a new one.

        Args:
            model_name: HuggingFace model identifier. Defaults to Settings.EMBEDDING_MODEL_NAME.

        Returns:
            Embeddings: Initialized LangChain compatible embedding model.

        Raises:
            EmbeddingError: If embedding model fails to initialize.
        """
        target_model = model_name or Settings.EMBEDDING_MODEL_NAME

        if cls._instance is not None:
            return cls._instance

        try:
            logger.info(f"Initializing HuggingFace embedding model: '{target_model}'")
            try:
                from langchain_huggingface import HuggingFaceEmbeddings
                cls._instance = HuggingFaceEmbeddings(
                    model_name=target_model,
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )
            except ImportError:
                logger.info("Fallback to langchain_community.embeddings.HuggingFaceEmbeddings")
                from langchain_community.embeddings import HuggingFaceEmbeddings
                cls._instance = HuggingFaceEmbeddings(
                    model_name=target_model,
                    model_kwargs={'device': 'cpu'},
                    encode_kwargs={'normalize_embeddings': True}
                )

            logger.info("Successfully initialized embedding model.")
            return cls._instance

        except Exception as e:
            logger.error(f"Failed to load embedding model '{target_model}': {str(e)}", exc_info=True)
            raise EmbeddingError(f"Embedding initialization error for model '{target_model}': {str(e)}") from e
