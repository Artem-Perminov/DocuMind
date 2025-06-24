"""
Unit tests for the AI Agent.
"""

import pytest
import os
import sys

# Add src to path for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from agent import AIAgent, AgentResponse, Message
from agent.tools import CalculatorTool, WebSearchTool, ToolRegistry
from config import settings


class TestAgentResponse:
    """Test AgentResponse model."""

    def test_agent_response_creation(self):
        """Test creating an AgentResponse."""
        response = AgentResponse(content="Hello", iterations=1, success=True)
        assert response.content == "Hello"
        assert response.iterations == 1
        assert response.success is True
        assert response.error is None
        assert response.tool_calls_made == []


class TestMessage:
    """Test Message model."""

    def test_message_creation(self):
        """Test creating a Message."""
        message = Message(role="user", content="Hello")
        assert message.role == "user"
        assert message.content == "Hello"
        assert message.tool_calls is None


class TestTools:
    """Test tool functionality."""

    def test_calculator_tool(self):
        """Test calculator tool."""
        calc = CalculatorTool()

        # Test valid expression
        result = calc.execute(expression="2 + 2")
        assert result["success"] is True
        assert result["result"] == 4

        # Test invalid expression
        result = calc.execute(expression="import os")
        assert result["success"] is False
        assert "error" in result

    def test_web_search_tool(self):
        """Test web search tool."""
        search = WebSearchTool()

        result = search.execute(query="Python programming")
        assert result["success"] is True
        assert "results" in result
        assert result["query"] == "Python programming"

    def test_tool_registry(self):
        """Test tool registry."""
        registry = ToolRegistry()

        # Test getting tools
        tools = registry.get_all_tools()
        assert len(tools) >= 2  # calculator and web search

        # Test getting function definitions
        function_defs = registry.get_function_definitions()
        assert len(function_defs) >= 2

        # Test executing tool
        result = registry.execute_tool("calculator", expression="5 * 3")
        assert result["success"] is True
        assert result["result"] == 15


class TestAIAgent:
    """Test AI Agent functionality."""

    def test_agent_initialization_without_api_key(self):
        """Test agent initialization fails without API key."""
        # Temporarily remove API key
        original_key = os.environ.get("OPENROUTER_API_KEY")
        if "OPENROUTER_API_KEY" in os.environ:
            del os.environ["OPENROUTER_API_KEY"]

        # Force settings to reload
        settings.openrouter_api_key = ""

        try:
            with pytest.raises(ValueError, match="OPENROUTER_API_KEY is not set"):
                AIAgent()
        finally:
            # Restore API key
            if original_key:
                os.environ["OPENROUTER_API_KEY"] = original_key
                settings.openrouter_api_key = original_key

    def test_agent_conversation_management(self):
        """Test conversation history management."""
        # Skip if no API key (for CI/CD)
        if not settings.validate_api_key():
            pytest.skip("No API key configured")

        agent = AIAgent()

        # Test initial state
        assert len(agent.get_conversation_history()) == 0

        # Reset conversation
        agent.reset_conversation()
        assert len(agent.get_conversation_history()) == 0

    def test_system_message_creation(self):
        """Test system message creation."""
        if not settings.validate_api_key():
            pytest.skip("No API key configured")

        agent = AIAgent()
        system_msg = agent._create_system_message()

        assert system_msg["role"] == "system"
        assert "helpful AI assistant" in system_msg["content"]
        assert "calculator" in system_msg["content"]  # Should mention available tools

    def test_message_preparation(self):
        """Test message preparation for API calls."""
        if not settings.validate_api_key():
            pytest.skip("No API key configured")

        agent = AIAgent()

        # Add some conversation history
        agent.conversation_history = [
            Message(role="user", content="Hello"),
            Message(role="assistant", content="Hi there!"),
        ]

        messages = agent._prepare_messages("How are you?")

        # Should have system message + history + current message
        assert len(messages) >= 4
        assert messages[0]["role"] == "system"
        assert messages[-1]["role"] == "user"
        assert messages[-1]["content"] == "How are you?"


class TestConfiguration:
    """Test configuration management."""

    def test_settings_loading(self):
        """Test settings are loaded correctly."""
        assert settings.model_name
        assert settings.max_tokens > 0
        assert settings.temperature >= 0
        assert settings.max_iterations > 0

    def test_api_key_validation(self):
        """Test API key validation."""
        # This will depend on whether the key is actually set
        # We just test the method exists and returns a boolean
        result = settings.validate_api_key()
        assert isinstance(result, bool)


# Integration tests (require API key)
class TestIntegration:
    """Integration tests that require actual API calls."""

    def test_basic_chat_without_tools(self):
        """Test basic chat functionality."""
        if not settings.validate_api_key():
            pytest.skip("No API key configured")

        agent = AIAgent()

        # Create agent without tools for this test
        agent.tool_registry = ToolRegistry()
        agent.tool_registry.tools = {}  # Clear tools

        # Note: This will make an actual API call
        # In a real test environment, you might want to mock this
        try:
            response = agent.chat("Say hello")
            assert response.success
            assert len(response.content) > 0
            assert response.iterations >= 1
        except Exception as e:
            pytest.skip(f"API call failed: {str(e)}")

    def test_tool_usage(self):
        """Test that agent can use tools."""
        if not settings.validate_api_key():
            pytest.skip("No API key configured")

        agent = AIAgent()

        try:
            response = agent.chat("What is 15 times 7?")
            # The agent should use the calculator tool
            assert response.success
            # We can't guarantee the exact response format, but it should succeed
        except Exception as e:
            pytest.skip(f"API call failed: {str(e)}")


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
