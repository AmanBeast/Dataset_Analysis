"""
Groq LLM Client Factory Module.

Provides ChatGroq LLM initialization, API key validation, and runtime error handling.
"""

import os
from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_groq import ChatGroq
from config.settings import Settings, logger
from core.exceptions import LLMConfigurationError

class GroqLLMFactory:
    """Factory for creating ChatGroq LLM client instances."""

    @staticmethod
    def get_llm(
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> BaseChatModel:
        """
        Instantiates ChatGroq model with key validation.

        Args:
            api_key: Groq API Key string. Defaults to Settings.GROQ_API_KEY or os.environ.
            model_name: Target model identifier. Defaults to Settings.GROQ_MODEL_NAME.
            temperature: LLM sampling temperature. Defaults to Settings.LLM_TEMPERATURE.

        Returns:
            BaseChatModel: Configured ChatGroq instance.

        Raises:
            LLMConfigurationError: If API key is missing.
        """
        key = api_key or Settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")

        if not key or not key.strip():
            logger.error("Groq API key is missing.")
            raise LLMConfigurationError(
                "Groq API Key is not set. Please provide a valid GROQ_API_KEY "
                "in your .env file or sidebar interface."
            )

        target_model = model_name or Settings.GROQ_MODEL_NAME
        temp = temperature if temperature is not None else Settings.LLM_TEMPERATURE

        try:
            logger.info(f"Initializing ChatGroq LLM (model='{target_model}', temperature={temp})")
            llm = ChatGroq(
                groq_api_key=key,
                model_name=target_model,
                temperature=temp,
                max_retries=2,
                timeout=30.0
            )
            return llm
        except Exception as e:
            logger.error(f"Failed to create ChatGroq client: {str(e)}", exc_info=True)
            raise LLMConfigurationError(f"Error configuring ChatGroq LLM: {str(e)}") from e
