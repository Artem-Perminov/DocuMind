"""
Basic tools for the AI Agent.
"""

import json
import requests
from typing import Dict, Any, List
from abc import ABC, abstractmethod


class Tool(ABC):
    """Base class for all tools."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        pass

    def to_function_def(self) -> Dict[str, Any]:
        """Convert tool to OpenAI function definition."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.get_parameters(),
            },
        }

    @abstractmethod
    def get_parameters(self) -> Dict[str, Any]:
        """Get tool parameters schema."""
        pass


class WebSearchTool(Tool):
    """Simple web search tool using DuckDuckGo."""

    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information on a given topic",
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"},
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5,
                },
            },
            "required": ["query"],
        }

    def execute(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Execute web search."""
        try:
            # This is a placeholder - replace with actual search API
            # For now, return mock data
            return {
                "success": True,
                "results": [
                    {
                        "title": f"Search result for: {query}",
                        "url": "https://example.com",
                        "snippet": f"This is a mock search result for the query: {query}",
                    }
                ],
                "query": query,
                "total_results": 1,
            }
        except Exception as e:
            return {"success": False, "error": str(e), "query": query}


class CalculatorTool(Tool):
    """Simple calculator tool."""

    def __init__(self):
        super().__init__(
            name="calculator", description="Perform basic mathematical calculations"
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate (e.g., '2 + 2', '10 * 5')",
                }
            },
            "required": ["expression"],
        }

    def execute(self, expression: str) -> Dict[str, Any]:
        """Execute calculation."""
        try:
            # Basic safety check
            if any(char in expression for char in ["import", "exec", "eval", "__"]):
                raise ValueError("Invalid expression")

            # Only allow basic math operations
            allowed_chars = set("0123456789+-*/(). ")
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Expression contains invalid characters")

            result = eval(expression)
            return {"success": True, "result": result, "expression": expression}
        except Exception as e:
            return {"success": False, "error": str(e), "expression": expression}


class ToolRegistry:
    """Registry for managing tools."""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register default tools."""
        self.register_tool(WebSearchTool())
        self.register_tool(CalculatorTool())

    def register_tool(self, tool: Tool):
        """Register a new tool."""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        """Get a tool by name."""
        return self.tools.get(name)

    def get_all_tools(self) -> List[Tool]:
        """Get all registered tools."""
        return list(self.tools.values())

    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Get function definitions for all tools."""
        return [tool.to_function_def() for tool in self.tools.values()]

    def execute_tool(self, name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool by name."""
        tool = self.get_tool(name)
        if not tool:
            return {"success": False, "error": f"Tool '{name}' not found"}

        return tool.execute(**kwargs)


# Global tool registry
tool_registry = ToolRegistry()
