"""
Custom Domain Exception Hierarchy.

Provides domain-specific exceptions for error tracking across PDF ingestion,
chunking, embedding generation, vector store persistence, and LLM execution.
"""

class DocumentIntelligenceError(Exception):
    """Base exception for all Document Intelligence errors."""
    pass

class PDFProcessingError(DocumentIntelligenceError):
    """Raised when PDF loading, reading, or validation fails."""
    pass

class InvalidPDFError(PDFProcessingError):
    """Raised when uploaded file is corrupt, non-PDF, or 0 bytes."""
    pass

class EmptyPDFError(PDFProcessingError):
    """Raised when PDF contains no extractable text pages."""
    pass

class EmbeddingError(DocumentIntelligenceError):
    """Raised when generating embeddings fails."""
    pass

class VectorStoreError(DocumentIntelligenceError):
    """Raised when FAISS index creation, saving, or loading fails."""
    pass

class LLMConfigurationError(DocumentIntelligenceError):
    """Raised when API key is missing or LLM parameters are invalid."""
    pass

class RAGChainError(DocumentIntelligenceError):
    """Raised when chain execution or prompt formatting fails."""
    pass
