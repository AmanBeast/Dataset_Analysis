"""
PDF Loader Module.

Encapsulates PDF document ingestion, format verification, and validation using PyPDFLoader.
Follows Single Responsibility Principle (SRP).
"""

from pathlib import Path
from typing import List, Union
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from config.settings import logger
from core.exceptions import InvalidPDFError, EmptyPDFError, PDFProcessingError

class PDFDocumentLoader:
    """
    Handles PDF document loading and validation.
    """

    def __init__(self, file_path: Union[str, Path]):
        """
        Initializes loader with PDF file path.

        Args:
            file_path: Path to the target PDF file.
        """
        self.file_path = Path(file_path)

    def validate_file(self) -> None:
        """
        Validates existence, extension, and non-zero byte size of the target PDF file.

        Raises:
            InvalidPDFError: If file doesn't exist, isn't a PDF, or is 0 bytes.
        """
        if not self.file_path.exists():
            logger.error(f"File not found: {self.file_path}")
            raise InvalidPDFError(f"PDF file does not exist at path: {self.file_path}")

        if not self.file_path.is_file():
            logger.error(f"Target is not a file: {self.file_path}")
            raise InvalidPDFError(f"Path is not a valid file: {self.file_path}")

        if self.file_path.suffix.lower() != ".pdf":
            logger.error(f"Invalid file extension: {self.file_path.suffix}")
            raise InvalidPDFError(f"File '{self.file_path.name}' is not a PDF file.")

        if self.file_path.stat().st_size == 0:
            logger.error(f"PDF file is 0 bytes: {self.file_path}")
            raise InvalidPDFError(f"PDF file '{self.file_path.name}' is empty (0 bytes).")

    def load(self) -> List[Document]:
        """
        Loads PDF content using PyPDFLoader and returns list of Document instances.

        Returns:
            List[Document]: Extracted pages as LangChain Documents.

        Raises:
            InvalidPDFError: If PDF validation fails.
            EmptyPDFError: If no extractable text is present.
            PDFProcessingError: If parsing fails due to corruption.
        """
        self.validate_file()

        try:
            logger.info(f"Loading PDF document: {self.file_path.name}")
            loader = PyPDFLoader(str(self.file_path))
            documents = loader.load()

            if not documents:
                logger.warning(f"No pages extracted from PDF: {self.file_path.name}")
                raise EmptyPDFError(f"PDF file '{self.file_path.name}' contains no readable pages.")

            # Filter out pages with completely empty content
            valid_docs = [doc for doc in documents if doc.page_content and doc.page_content.strip()]
            if not valid_docs:
                logger.warning(f"No text content found in PDF pages: {self.file_path.name}")
                raise EmptyPDFError(f"PDF file '{self.file_path.name}' contains no extractable text.")

            logger.info(f"Successfully loaded {len(valid_docs)} pages from {self.file_path.name}")
            return valid_docs

        except (InvalidPDFError, EmptyPDFError):
            raise
        except Exception as e:
            logger.error(f"Error reading PDF file {self.file_path.name}: {str(e)}", exc_info=True)
            raise PDFProcessingError(f"Failed to process corrupted or unreadable PDF: {str(e)}") from e
