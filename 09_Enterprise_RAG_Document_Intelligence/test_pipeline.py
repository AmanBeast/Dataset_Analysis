"""
Automated Test Suite for Document Intelligence RAG System.

Validates PDF loading, document chunking, embedding generation,
FAISS vector indexing, disk caching, similarity search, and RAG execution.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from config.settings import Settings, logger
from core.exceptions import InvalidPDFError, EmptyPDFError, LLMConfigurationError
from loaders.pdf_loader import PDFDocumentLoader
from splitters.chunking import DocumentSplitter
from embeddings.embedding_model import EmbeddingModelFactory
from vectorstore.faiss_store import FAISSVectorStoreManager
from services.document_service import DocumentProcessingService
from services.qa_service import RetrievalQAService
from utils.helpers import compute_file_hash, extract_source_pages, format_retrieved_chunks

TEST_PDF_PATH = BASE_DIR / "final_assessment_langchain.pdf"

class TestDocumentIntelligencePipeline(unittest.TestCase):
    """Integration and Unit Test Suite."""

    def setUp(self):
        """Pre-test check."""
        self.assertTrue(TEST_PDF_PATH.exists(), f"Sample PDF missing at {TEST_PDF_PATH}")

    def test_01_file_hash_computation(self):
        """Tests MD5 hash generation for caching."""
        pdf_hash = compute_file_hash(TEST_PDF_PATH)
        self.assertIsInstance(pdf_hash, str)
        self.assertEqual(len(pdf_hash), 32)
        logger.info(f"Test 01 Passed: MD5 Hash = {pdf_hash}")

    def test_02_pdf_loader(self):
        """Tests PyPDFLoader loading and page extraction."""
        loader = PDFDocumentLoader(TEST_PDF_PATH)
        documents = loader.load()
        self.assertGreater(len(documents), 0, "Loader returned empty list of pages.")
        self.assertIsNotNone(documents[0].page_content)
        self.assertTrue(len(documents[0].page_content.strip()) > 0)
        logger.info(f"Test 02 Passed: Loaded {len(documents)} pages.")

    def test_03_document_splitter(self):
        """Tests RecursiveCharacterTextSplitter chunking logic."""
        loader = PDFDocumentLoader(TEST_PDF_PATH)
        docs = loader.load()
        splitter = DocumentSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        self.assertGreaterEqual(len(chunks), len(docs), "Chunks count should be >= page count.")
        logger.info(f"Test 03 Passed: Generated {len(chunks)} chunks.")

    def test_04_embedding_model(self):
        """Tests HuggingFace embedding model initialization and vector generation."""
        model = EmbeddingModelFactory.get_embedding_model()
        self.assertIsNotNone(model)
        sample_vector = model.embed_query("Document intelligence system test query")
        self.assertEqual(len(sample_vector), 384, "all-MiniLM-L6-v2 vector dimension must be 384.")
        logger.info(f"Test 04 Passed: Embedding vector generated (dim={len(sample_vector)}).")

    def test_05_faiss_vectorstore_and_caching(self):
        """Tests FAISS index creation, disk serialization, and cached loading."""
        doc_service = DocumentProcessingService(chunk_size=1000, chunk_overlap=100)
        result = doc_service.process_pdf(TEST_PDF_PATH, filename=TEST_PDF_PATH.name)

        self.assertIn("vectorstore", result)
        self.assertIn("retriever", result)
        self.assertIn("file_hash", result)

        file_hash = result["file_hash"]

        # Verify second call triggers cache hit
        cached_result = doc_service.process_pdf(TEST_PDF_PATH, filename=TEST_PDF_PATH.name)
        self.assertTrue(cached_result["is_cached"], "Second call with same file must hit FAISS cache.")
        logger.info("Test 05 Passed: FAISS index build and disk cache reload verified.")

    def test_06_similarity_retrieval(self):
        """Tests vector search retrieval on FAISS index."""
        doc_service = DocumentProcessingService()
        result = doc_service.process_pdf(TEST_PDF_PATH, filename=TEST_PDF_PATH.name)
        retriever = result["retriever"]

        docs = retriever.invoke("What is the goal of this project?")
        self.assertGreater(len(docs), 0, "Retriever returned 0 chunks for query.")
        pages = extract_source_pages(docs)
        self.assertIsInstance(pages, list)
        logger.info(f"Test 06 Passed: Retrieved {len(docs)} relevant chunks across pages {pages}.")

    def test_07_rag_chain_execution(self):
        """Tests end-to-end RAG query execution if GROQ_API_KEY is available."""
        api_key = os.getenv("GROQ_API_KEY", "")
        if not api_key:
            logger.warning("GROQ_API_KEY not set. Skipping live ChatGroq LLM call test.")
            return

        doc_service = DocumentProcessingService()
        result = doc_service.process_pdf(TEST_PDF_PATH, filename=TEST_PDF_PATH.name)
        retriever = result["retriever"]

        qa_service = RetrievalQAService(retriever=retriever, api_key=api_key)
        response = qa_service.answer_question("Summarize the main topic of this document.")

        self.assertIn("answer", response)
        self.assertIn("source_pages", response)
        self.assertIn("retrieved_chunks", response)
        self.assertTrue(len(response["answer"]) > 0)
        logger.info(f"Test 07 Passed: Live ChatGroq RAG response generated:\n{response['answer']}")

if __name__ == "__main__":
    unittest.main(verbosity=2)
