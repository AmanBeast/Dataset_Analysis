"""
LCEL RAG Chain Module.

Builds and executes LCEL (LangChain Expression Language) retrieval chains,
formatting context with page annotations and returning structured answers with metadata.
"""

from typing import Dict, Any, List
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from prompts.prompt_template import get_rag_prompt_template
from utils.helpers import extract_source_pages, format_retrieved_chunks
from config.settings import logger
from core.exceptions import RAGChainError

def format_context_docs(documents: List[Document]) -> str:
    """
    Formats a list of Document objects into a single context string with explicit page headers.

    Args:
        documents: List of retrieved Document chunks.

    Returns:
        Formatted context string.
    """
    formatted_chunks = []
    for doc in documents:
        page = doc.metadata.get("page", 0)
        page_num = page + 1 if isinstance(page, int) else page
        formatted_chunks.append(f"--- [SOURCE PAGE: {page_num}] ---\n{doc.page_content.strip()}")
    return "\n\n".join(formatted_chunks)

class DocumentIntelligenceRAGChain:
    """
    LCEL RAG Chain Manager.
    Coordinates retriever, prompt template, and LLM to produce answers with full citation metadata.
    """

    def __init__(self, retriever: VectorStoreRetriever, llm: BaseChatModel):
        """
        Initializes RAG chain with retriever and LLM instances.

        Args:
            retriever: VectorStoreRetriever instance.
            llm: Configured LLM (e.g. ChatGroq).
        """
        self.retriever = retriever
        self.llm = llm
        self.prompt = get_rag_prompt_template()

    def run(self, query: str) -> Dict[str, Any]:
        """
        Executes RAG pipeline for a given user query.

        Steps:
        1. Retrieve relevant chunks from vectorstore.
        2. Format context with source page markers.
        3. Pass context and query through LLM.
        4. Extract source page numbers and format retrieved chunks.

        Args:
            query: User's question string.

        Returns:
            Dict containing:
                - 'query': Original user question
                - 'answer': Generated LLM answer string
                - 'source_pages': Sorted list of 1-indexed page numbers
                - 'retrieved_chunks': List of formatted chunk dicts
                - 'raw_documents': List of raw LangChain Document objects

        Raises:
            RAGChainError: If chain execution fails.
        """
        if not query or not query.strip():
            raise RAGChainError("User query cannot be empty.")

        try:
            logger.info(f"Executing RAG query: '{query[:60]}...'")

            # 1. Retrieve documents directly to preserve metadata and return raw chunks
            retrieved_docs: List[Document] = self.retriever.invoke(query)
            logger.info(f"Retrieved {len(retrieved_docs)} context chunks for query.")

            if not retrieved_docs:
                return {
                    "query": query,
                    "answer": "I couldn't find that information in the uploaded document.",
                    "source_pages": [],
                    "retrieved_chunks": [],
                    "raw_documents": []
                }

            # 2. Format context string
            context_str = format_context_docs(retrieved_docs)

            # 3. Construct LCEL runnable chain
            lcel_chain = (
                self.prompt
                | self.llm
                | StrOutputParser()
            )

            # 4. Invoke LLM with formatted context and user query
            answer_str = lcel_chain.invoke({
                "context": context_str,
                "question": query
            })

            # 5. Extract page numbers and chunk metadata
            source_pages = extract_source_pages(retrieved_docs)
            formatted_chunks = format_retrieved_chunks(retrieved_docs)

            logger.info(f"RAG query completed successfully. Referenced pages: {source_pages}")

            return {
                "query": query,
                "answer": answer_str.strip(),
                "source_pages": source_pages,
                "retrieved_chunks": formatted_chunks,
                "raw_documents": retrieved_docs
            }

        except Exception as e:
            logger.error(f"Error executing RAG chain query: {str(e)}", exc_info=True)
            raise RAGChainError(f"RAG execution failure: {str(e)}") from e
