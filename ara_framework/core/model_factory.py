"""
Model Factory - Create LLM instances for different providers.

This module centralizes LLM creation logic to make it easy to switch
between providers (GitHub Models, Ollama, Groq, etc.) for testing and production.
"""

import structlog
from typing import Optional, List, Literal
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from config.settings import settings

logger = structlog.get_logger(__name__)


def create_github_model(
    model: Optional[str] = None,
    temperature: float = 0.7,
) -> ChatOpenAI:
    """
    Create a ChatOpenAI instance configured for GitHub Models.
    
    Args:
        model: Model name (default: settings.GITHUB_MODEL)
        temperature: Temperature for sampling (default: 0.7)
    
    Returns:
        Configured ChatOpenAI instance
    
    Example:
        >>> llm = create_github_model(model="gpt-4o", temperature=0.7)
    """
    return ChatOpenAI(
        model=model or settings.GITHUB_MODEL,
        temperature=temperature,
        api_key=settings.GITHUB_TOKEN,
        base_url=settings.GITHUB_MODELS_BASE_URL,
    )


def create_ollama_model(
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    num_ctx: Optional[int] = None,
) -> ChatOllama:
    """
    Create a ChatOllama instance for local Ollama models.
    
    Args:
        model: Model name (default: settings.OLLAMA_MODEL = "mistral:7b")
        temperature: Temperature for sampling (default: settings.OLLAMA_TEMPERATURE)
        num_ctx: Context window size (default: settings.OLLAMA_NUM_CTX = 32768)
    
    Returns:
        Configured ChatOllama instance
    
    Example:
        >>> llm = create_ollama_model(model="mistral:7b")
        >>> # With custom context window
        >>> llm = create_ollama_model(model="qwen2.5:8b", num_ctx=65536)
    
    Note:
        Requires Ollama server running: `ollama serve`
        And model downloaded: `ollama pull mistral:7b`
    """
    model_name = model or settings.OLLAMA_MODEL
    
    logger.info(
        "Creating Ollama model",
        model=model_name,
        base_url=settings.OLLAMA_BASE_URL,
        num_ctx=num_ctx or settings.OLLAMA_NUM_CTX,
    )
    
    return ChatOllama(
        model=model_name,
        temperature=temperature or settings.OLLAMA_TEMPERATURE,
        base_url=settings.OLLAMA_BASE_URL,
        num_ctx=num_ctx or settings.OLLAMA_NUM_CTX,
    )


def create_model(
    provider: Literal["github", "ollama"] = "github",
    model: Optional[str] = None,
    temperature: float = 0.7,
    **kwargs,
) -> BaseChatModel:
    """
    Universal model factory - create LLM for any provider.
    
    Args:
        provider: Provider name ("github" or "ollama")
        model: Model name (provider-specific)
        temperature: Temperature for sampling
        **kwargs: Additional provider-specific arguments
    
    Returns:
        Configured LLM instance
    
    Example:
        >>> # GitHub Models (production)
        >>> llm = create_model(provider="github", model="gpt-4o")
        >>> 
        >>> # Ollama (testing)
        >>> llm = create_model(provider="ollama", model="mistral:7b", num_ctx=32768)
    
    Raises:
        ValueError: If provider is not supported
    """
    if provider == "github":
        return create_github_model(model=model, temperature=temperature)
    elif provider == "ollama":
        return create_ollama_model(
            model=model,
            temperature=temperature,
            num_ctx=kwargs.get("num_ctx"),
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def bind_tools_safe(
    llm: BaseChatModel,
    tools: List[BaseTool],
) -> BaseChatModel:
    """
    Safely bind tools to an LLM, handling provider-specific issues.
    
    Args:
        llm: LLM instance
        tools: List of LangChain tools
    
    Returns:
        LLM with tools bound
    
    Example:
        >>> from tools.search_tool import search_recent_papers
        >>> llm = create_model(provider="ollama", model="mistral:7b")
        >>> llm_with_tools = bind_tools_safe(llm, [search_recent_papers])
    
    Note:
        Ollama models require special handling for tool calling.
        This function abstracts those differences.
    """
    try:
        return llm.bind_tools(tools)
    except Exception as e:
        logger.error(
            "Failed to bind tools",
            error=str(e),
            llm_type=type(llm).__name__,
            num_tools=len(tools),
        )
        raise


def verify_model_availability(
    provider: Literal["github", "ollama"] = "github",
    model: Optional[str] = None,
) -> bool:
    """
    Verify that a model is available and working.
    
    Args:
        provider: Provider name
        model: Model name
    
    Returns:
        True if model is available and responds
    
    Example:
        >>> if verify_model_availability("ollama", "mistral:7b"):
        >>>     print("Mistral is ready!")
    """
    try:
        llm = create_model(provider=provider, model=model)
        response = llm.invoke("Test")
        return len(response.content) > 0
    except Exception as e:
        logger.error(
            "Model verification failed",
            provider=provider,
            model=model,
            error=str(e),
        )
        return False
