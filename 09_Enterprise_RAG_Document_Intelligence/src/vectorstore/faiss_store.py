"""
FAISS Vector Store Manager Module.

Handles FAISS vector index creation, disk serialization, hash-based caching,
and retriever construction.
"""

from pathlib import Path
from typing import List, Optional
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_community.vectorstores import FAISS
from config.settings import Settings, logger
from core.exceptions import VectorStoreError

class FAISSVectorStoreManager:
    """
    Manages local FAISS vectorstore instances, index persistence, and retrievers.
    """

    def __init__(self, embeddings: Embeddings, cache_dir: Optional[Path] = None):
        """
        Initializes FAISS store manager.

        Args:
            embeddings: LangChain Embeddings instance.
            cache_dir: Optional custom cache directory path.
        """
        self.embeddings = embeddings
        self.cache_dir = cache_dir or Settings.CACHE_DIR
        self.vectorstore: Optional[FAISS] = None

    def get_cache_path(self, file_hash: str) -> Path:
        """Returns directory path for a specific file hash cache."""
        return self.cache_dir / file_hash

    def is_cached(self, file_hash: str) -> bool:
        """Checks whether a valid FAISS index cache exists for a file hash."""
        cache_path = self.get_cache_path(file_hash)
        faiss_file = cache_path / "index.faiss"
        pkl_file = cache_path / "index.pkl"
        return cache_path.exists() and faiss_file.exists() and pkl_file.exists()

    def build_from_documents(self, documents: List[Document], file_hash: Optional[str] = None) -> FAISS:
        """
        Builds FAISS index from document chunks and caches it to disk if file_hash is supplied.

        Args:
            documents: List of chunked Document instances.
            file_hash: Optional MD5 checksum string for disk caching.

        Returns:
            FAISS: Created vectorstore instance.

        Raises:
            VectorStoreError: If FAISS index creation fails.
        """
        if not documents:
            raise VectorStoreError("Cannot build FAISS store from empty document list.")

        try:
            logger.info(f"Generating FAISS vector index for {len(documents)} chunks...")
            self.vectorstore = FAISS.from_documents(documents, self.embeddings)

            if file_hash:
                cache_path = self.get_cache_path(file_hash)
                logger.info(f"Saving FAISS index cache to: {cache_path}")
                cache_path.mkdir(parents=True, exist_ok=True)
                self.vectorstore.save_local(str(cache_path))

            return self.vectorstore

        except Exception as e:
            logger.error(f"Error creating FAISS vectorstore: {str(e)}", exc_info=True)
            raise VectorStoreError(f"Failed to generate FAISS vector index: {str(e)}") from e

    def load_from_cache(self, file_hash: str) -> FAISS:
        """
        Loads FAISS index from local disk cache.

        Args:
            file_hash: MD5 hash key identifying the cache directory.

        Returns:
            FAISS: Loaded vectorstore instance.

        Raises:
            VectorStoreError: If loading from cache fails.
        """
        cache_path = self.get_cache_path(file_hash)
        if not self.is_cached(file_hash):
            raise VectorStoreError(f"No FAISS index cache found at: {cache_path}")

        try:
            logger.info(f"Loading cached FAISS index from: {cache_path}")
            self.vectorstore = FAISS.load_local(
                str(cache_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            logger.info("Successfully loaded FAISS index from cache.")
            return self.vectorstore
        except Exception as e:
            logger.error(f"Failed to load cached FAISS store: {str(e)}", exc_info=True)
            raise VectorStoreError(f"FAISS index load error: {str(e)}") from e

    def get_or_create(self, documents: List[Document], file_hash: str) -> FAISS:
        """
        Loads cached FAISS index if available; otherwise builds and caches a new index.

        Args:
            documents: List of Document chunks.
            file_hash: MD5 file hash key.

        Returns:
            FAISS: Ready-to-use vectorstore.
        """
        if self.is_cached(file_hash):
            return self.load_from_cache(file_hash)
        return self.build_from_documents(documents, file_hash=file_hash)

    def get_retriever(
        self,
        vectorstore: Optional[FAISS] = None,
        search_type: str = "similarity",
        k: int = Settings.RETRIEVER_K
    ) -> VectorStoreRetriever:
        """
        Creates a retriever interface over the FAISS store.

        Args:
            vectorstore: Target FAISS store. Uses self.vectorstore if None.
            search_type: Retrieval strategy ('similarity' or 'mmr').
            k: Top k documents to retrieve.

        Returns:
            VectorStoreRetriever: LangChain retriever instance.
        """
        target_store = vectorstore or self.vectorstore
        if target_store is None:
            raise VectorStoreError("Vector store is not initialized. Build or load an index first.")

        logger.info(f"Creating retriever strategy='{search_type}' with k={k}")
        return target_store.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )
