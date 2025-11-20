"""
Perplexity API Tool - Real-time web search with LLM processing.

Perplexity combines web search with LLM inference, providing:
- Real-time web results
- LLM-processed summaries
- Citations and sources
- No need for separate scraping

Best for:
- Current events and trends
- Recent developments (last 24-48 hours)
- Community discussions
- Market analysis

Usage:
    from tools.perplexity_tool import perplexity_search
    
    result = await perplexity_search(
        query="Latest trends in Rust WebAssembly",
        search_recency_filter="month"
    )
"""

import structlog
from typing import Optional, Literal
from langchain_core.tools import tool
from openai import OpenAI

from config.settings import settings

logger = structlog.get_logger(__name__)


@tool("perplexity_search")
async def perplexity_search(
    query: str,
    search_recency_filter: Optional[Literal["month", "week", "day"]] = "month",
    max_tokens: int = 2000,
) -> str:
    """
    Search the web using Perplexity AI with real-time results and LLM processing.
    
    This tool combines web search with language model inference to provide
    comprehensive, up-to-date information with citations.
    
    Args:
        query: The search query (e.g., "Latest trends in Rust WebAssembly")
        search_recency_filter: Time filter for results
            - "month": Results from last 30 days (default)
            - "week": Results from last 7 days
            - "day": Results from last 24 hours
        max_tokens: Maximum response length (default: 2000)
    
    Returns:
        Formatted response with web results, analysis, and citations.
        
    Examples:
        >>> result = await perplexity_search(
        ...     query="Rust WebAssembly real-time audio processing trends",
        ...     search_recency_filter="month"
        ... )
        >>> print(result)
        
    Note:
        - Requires PERPLEXITY_API_KEY in environment
        - Uses "llama-3.1-sonar-large-128k-online" model by default
        - Includes automatic citation extraction
    """
    
    if not settings.PERPLEXITY_API_KEY:
        logger.warning("perplexity_api_key_missing")
        return "⚠️ Perplexity API key not configured. Please set PERPLEXITY_API_KEY environment variable."
    
    try:
        logger.info(
            "executing_perplexity_search",
            query=query,
            recency_filter=search_recency_filter,
        )
        
        # Initialize Perplexity client (OpenAI-compatible)
        client = OpenAI(
            api_key=settings.PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai",
        )
        
        # Perplexity models:
        # - llama-3.1-sonar-small-128k-online: Fast, cheaper
        # - llama-3.1-sonar-large-128k-online: Better quality (recommended)
        # - llama-3.1-sonar-huge-128k-online: Best quality, slower
        
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful research assistant. "
                    "Provide comprehensive, well-structured information with citations. "
                    "Focus on recent developments, trends, and actionable insights."
                ),
            },
            {
                "role": "user",
                "content": query,
            },
        ]
        
        # Call Perplexity API
        response = client.chat.completions.create(
            model=settings.PERPLEXITY_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,  # Lower for factual accuracy
            top_p=0.9,
            search_recency_filter=search_recency_filter,
            return_citations=True,
            return_images=False,
            return_related_questions=True,
        )
        
        # Extract response
        content = response.choices[0].message.content
        
        # Extract citations if available
        citations = []
        if hasattr(response, "citations") and response.citations:
            citations = response.citations
        
        # Extract related questions if available
        related_questions = []
        if hasattr(response, "related_questions") and response.related_questions:
            related_questions = response.related_questions
        
        # Format response
        formatted_response = f"""# Perplexity Search Results

**Query**: {query}
**Recency Filter**: {search_recency_filter}

## Summary

{content}
"""
        
        # Add citations
        if citations:
            formatted_response += "\n\n## Citations\n\n"
            for i, citation in enumerate(citations, 1):
                formatted_response += f"{i}. {citation}\n"
        
        # Add related questions
        if related_questions:
            formatted_response += "\n\n## Related Questions\n\n"
            for question in related_questions:
                formatted_response += f"- {question}\n"
        
        logger.info(
            "perplexity_search_completed",
            query=query,
            response_length=len(content),
            citations_count=len(citations),
            related_questions_count=len(related_questions),
        )
        
        return formatted_response
        
    except Exception as e:
        error_msg = str(e)
        logger.error(
            "perplexity_search_failed",
            query=query,
            error=error_msg,
            error_type=type(e).__name__,
        )
        
        return f"❌ Perplexity search failed: {error_msg}"


@tool("perplexity_search_fast")
async def perplexity_search_fast(
    query: str,
    max_tokens: int = 1000,
) -> str:
    """
    Fast web search using Perplexity AI (smaller model, quicker results).
    
    Uses the smaller "sonar-small" model for faster responses.
    Best for quick lookups and when response time is critical.
    
    Args:
        query: The search query
        max_tokens: Maximum response length (default: 1000)
    
    Returns:
        Brief formatted response with web results.
    """
    
    if not settings.PERPLEXITY_API_KEY:
        logger.warning("perplexity_api_key_missing")
        return "⚠️ Perplexity API key not configured."
    
    try:
        logger.info("executing_perplexity_search_fast", query=query)
        
        client = OpenAI(
            api_key=settings.PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai",
        )
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Provide concise, accurate information.",
            },
            {
                "role": "user",
                "content": query,
            },
        ]
        
        response = client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",  # Fast model
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2,
            search_recency_filter="month",
            return_citations=True,
        )
        
        content = response.choices[0].message.content
        
        logger.info(
            "perplexity_search_fast_completed",
            query=query,
            response_length=len(content),
        )
        
        return f"**Search Results**: {query}\n\n{content}"
        
    except Exception as e:
        logger.error(
            "perplexity_search_fast_failed",
            query=query,
            error=str(e),
        )
        return f"❌ Fast search failed: {str(e)}"


# Singleton pattern - reuse client across calls
_perplexity_client: Optional[OpenAI] = None


def get_perplexity_client() -> Optional[OpenAI]:
    """Get or create Perplexity client (singleton pattern)."""
    global _perplexity_client
    
    if not settings.PERPLEXITY_API_KEY:
        return None
    
    if _perplexity_client is None:
        _perplexity_client = OpenAI(
            api_key=settings.PERPLEXITY_API_KEY,
            base_url="https://api.perplexity.ai",
        )
        logger.info("perplexity_client_initialized")
    
    return _perplexity_client
