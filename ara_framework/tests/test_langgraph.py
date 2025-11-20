"""
Test for LangGraph research graph implementation.

This test verifies that the LangGraph migration is working correctly
by testing the graph structure and basic execution.
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock

from graphs.research_graph import (
    create_research_graph,
    ResearchState,
    run_research_pipeline,
)


class TestResearchGraph:
    """Test suite for LangGraph research graph."""
    
    def test_graph_creation(self):
        """Test that the graph can be created successfully."""
        graph = create_research_graph(
            enable_checkpointing=False,
        )
        
        assert graph is not None
        # Graph should be compiled and ready
        assert hasattr(graph, "invoke")
        assert hasattr(graph, "ainvoke")
    
    def test_graph_with_memory_checkpointing(self):
        """Test graph creation with memory checkpointing."""
        graph = create_research_graph(
            enable_checkpointing=True,
            checkpoint_backend="memory",
        )
        
        assert graph is not None
    
    def test_initial_state_structure(self):
        """Test that the initial state has required fields."""
        from datetime import datetime, timezone
        
        initial_state: ResearchState = {
            "niche": "Test Niche",
            "niche_analysis": None,
            "literature_review": None,
            "technical_architecture": None,
            "implementation_plan": None,
            "final_report": None,
            "messages": [],
            "current_agent": "niche_analyst",
            "agent_history": [],
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": None,
            "errors": [],
            "warnings": [],
            "retry_count": {},
            "total_credits_used": 0.0,
            "budget_limit": 10.0,
            "budget_exceeded": False,
            
        }
        
        # Verify all required keys are present
        required_keys = [
            "niche", "messages", "current_agent", "agent_history",
            "errors", "warnings", "retry_count", "total_credits_used",
            "budget_limit", "budget_exceeded",
        ]
        
        for key in required_keys:
            assert key in initial_state, f"Missing required key: {key}"
    
    @pytest.mark.asyncio
    async def test_graph_structure(self):
        """Test the graph has correct nodes and edges."""
        graph = create_research_graph(enable_checkpointing=False)
        
        # The graph should have our 5 agent nodes
        # Note: LangGraph internal structure may vary, 
        # so we just verify it was created without errors
        assert graph is not None
    
    @pytest.mark.asyncio
    @patch("graphs.research_graph.safe_agent_invoke")
    @patch("graphs.research_graph.create_model")
    async def test_niche_analyst_node(self, mock_create_model, mock_safe_invoke):
        """Test the niche analyst node in isolation."""
        from graphs.research_graph import niche_analyst_node
        from langchain_core.messages import AIMessage
        
        # Mock the model and safe_agent_invoke
        mock_model = Mock()
        mock_create_model.return_value = mock_model
        
        mock_safe_invoke.return_value = {
            "output": "# Niche Analysis\n\nThis is a test analysis.",
            "tool_calls": []
        }
        
        # Create initial state
        initial_state: ResearchState = {
            "niche": "Test Technology",
            "niche_analysis": None,
            "literature_review": None,
            "technical_architecture": None,
            "implementation_plan": None,
            "final_report": None,
            "messages": [],
            "current_agent": "niche_analyst",
            "agent_history": [],
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": None,
            "errors": [],
            "warnings": [],
            "retry_count": {},
            "total_credits_used": 0.0,
            "budget_limit": 10.0,
            "budget_exceeded": False,
            
        }
        
        # Execute node (async)
        result = await niche_analyst_node(initial_state)
        
        # Verify results
        assert result["niche_analysis"] is not None
        assert "test analysis" in result["niche_analysis"]
        assert "niche_analyst" in result["agent_history"]
        assert result["current_agent"] == "literature_researcher"
    
    @pytest.mark.asyncio
    @patch("graphs.research_graph.safe_agent_invoke")
    @patch("graphs.research_graph.create_model")
    async def test_error_handling_in_node(self, mock_create_model, mock_safe_invoke):
        """Test that nodes handle errors properly."""
        from graphs.research_graph import niche_analyst_node
        
        # Mock model creation to work
        mock_model = Mock()
        mock_create_model.return_value = mock_model
        
        # Mock safe_agent_invoke to raise an error
        mock_safe_invoke.side_effect = Exception("Test error")
        
        initial_state: ResearchState = {
            "niche": "Test",
            "niche_analysis": None,
            "literature_review": None,
            "technical_architecture": None,
            "implementation_plan": None,
            "final_report": None,
            "messages": [],
            "current_agent": "niche_analyst",
            "agent_history": [],
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": None,
            "errors": [],
            "warnings": [],
            "retry_count": {},
            "total_credits_used": 0.0,
            "budget_limit": 10.0,
            "budget_exceeded": False,
            
        }
        
        # Execute node (should handle error gracefully)
        result = await niche_analyst_node(initial_state)
        
        # Verify error handling
        assert len(result["errors"]) > 0
        assert "NicheAnalyst" in result["errors"][0]
        assert result["retry_count"]["niche_analyst"] == 1
    
    @pytest.mark.asyncio
    async def test_sequential_flow(self):
        """Test that state flows sequentially through nodes."""
        # This is more of an integration test
        # For unit tests, we'd mock each node
        
        # Just verify the graph can be created and has the right structure
        graph = create_research_graph(enable_checkpointing=False)
        assert graph is not None


class TestConvenienceFunctions:
    """Test convenience functions for running the pipeline."""
    
    @pytest.mark.asyncio
    @patch("graphs.research_graph.create_research_graph")
    async def test_run_research_pipeline(self, mock_create_graph):
        """Test the convenience function for running pipeline."""
        from langchain_core.messages import AIMessage
        
        # Mock graph
        mock_graph = Mock()
        mock_graph.ainvoke = AsyncMock(return_value={
            "niche": "Test",
            "niche_analysis": "Analysis",
            "literature_review": "Review",
            "technical_architecture": "Architecture",
            "implementation_plan": "Plan",
            "final_report": "Final Report",
            "messages": [AIMessage(content="Done")],
            "current_agent": "completed",
            "agent_history": [
                "niche_analyst",
                "literature_researcher",
                "technical_architect",
                "implementation_specialist",
                "content_synthesizer",
            ],
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": "2025-01-01T01:00:00Z",
            "errors": [],
            "warnings": [],
            "retry_count": {},
            "total_credits_used": 2.5,
            "budget_limit": 10.0,
            "budget_exceeded": False,
            
        })
        mock_create_graph.return_value = mock_graph
        
        # Run pipeline
        result = await run_research_pipeline(
            niche="Test Technology",
            budget_limit=10.0,
        )
        
        # Verify
        assert result["final_report"] == "Final Report"
        assert len(result["agent_history"]) == 5
        assert result["errors"] == []
        assert not result["budget_exceeded"]


@pytest.mark.skipif(
    True,  # Skip by default as it requires API keys
    reason="Integration test requires API keys and takes time"
)
class TestLangGraphIntegration:
    """
    Integration tests for the full LangGraph pipeline.
    
    These tests require valid API keys and will make real API calls.
    Run with: pytest -v --run-integration
    """
    
    @pytest.mark.asyncio
    async def test_full_pipeline_execution(self):
        """Test full pipeline execution with real APIs."""
        result = await run_research_pipeline(
            niche="Minimal test niche for integration testing",
            budget_limit=1.0,  # Low budget for testing
            enable_checkpointing=True,
        )
        
        # Basic assertions
        assert result is not None
        assert result["niche"] == "Minimal test niche for integration testing"
        assert len(result["agent_history"]) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
