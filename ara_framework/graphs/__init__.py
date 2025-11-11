"""
LangGraph-based workflow graphs for ARA Framework.

This module contains graph implementations for multi-agent research workflows
using LangGraph, the production-ready framework for complex agent orchestration.

Available Graphs:
- ResearchGraph: Main 5-agent research pipeline
"""

from graphs.research_graph import create_research_graph, ResearchState

__all__ = [
    "create_research_graph",
    "ResearchState",
]
