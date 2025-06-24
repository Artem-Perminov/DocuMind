"""
Core AI Agent implementation.
"""

import json
import logging
import time
from typing import Dict, Any, List, Optional
from openai import OpenAI
from pydantic import BaseModel

from config import settings
from .tools import tool_registry as global_tool_registry, ToolRegistry


# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)


class Message(BaseModel):
    """Represents a conversation message."""

    role: str
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None


class AgentResponse(BaseModel):
    """Represents an agent response."""

    content: str
    tool_calls_made: List[Dict[str, Any]] = []
    iterations: int = 0
    success: bool = True
    error: Optional[str] = None


class AIAgent:
    """
    Simple AI Agent with tool integration capabilities.

    This agent uses the ReAct pattern (Reasoning + Acting) to:
    1. Reason about the user's request
    2. Decide which tools to use (if any)
    3. Execute tools
    4. Provide a final response
    """

    def __init__(self, tool_registry: Optional[ToolRegistry] = None):
        """Initialize the AI Agent."""
        if not settings.validate_api_key():
            raise ValueError("OPENROUTER_API_KEY is not set or invalid")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )

        self.tool_registry = (
            tool_registry if tool_registry is not None else global_tool_registry
        )
        self.conversation_history: List[Message] = []

        logger.info(f"AI Agent initialized with model: {settings.model_name}")

    def _create_system_message(self) -> Dict[str, str]:
        """Create the system message for the agent."""
        tools_description = ""
        if self.tool_registry.get_all_tools():
            tool_names = [tool.name for tool in self.tool_registry.get_all_tools()]
            tools_description = f"\n\nYou have access to the following tools: {', '.join(tool_names)}. Use them when they would be helpful to answer the user's question."

        return {
            "role": "system",
            "content": f"""You are a helpful AI assistant. You can engage in conversations and help users with various tasks.{tools_description}

When using tools:
1. Think step by step about what information you need
2. Use tools when they would provide helpful information
3. Always provide a clear, helpful response to the user

Be concise but thorough in your responses.""",
        }

    def _prepare_messages(self, user_message: str) -> List[Dict[str, Any]]:
        """Prepare messages for the API call."""
        messages = [self._create_system_message()]

        # Add conversation history
        for msg in self.conversation_history[-5:]:  # Keep last 5 messages for context
            messages.append({"role": msg.role, "content": msg.content})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        return messages

    def _make_api_call(
        self, messages: List[Dict[str, Any]], use_tools: bool = True
    ) -> Any:
        """Make an API call to the language model."""
        try:
            call_params = {
                "model": settings.model_name,
                "messages": messages,
                "max_tokens": settings.max_tokens,
                "temperature": settings.temperature,
                "extra_headers": {
                    "HTTP-Referer": settings.site_url,
                    "X-Title": settings.site_name,
                },
            }

            # Add tools if available and requested
            if use_tools and self.tool_registry.get_all_tools():
                call_params["tools"] = self.tool_registry.get_function_definitions()
                call_params["tool_choice"] = "auto"

            response = self.client.chat.completions.create(**call_params)
            return response

        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            raise

    def _execute_tool_calls(
        self, tool_calls: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute tool calls and return results."""
        results = []

        for tool_call in tool_calls:
            try:
                function_name = tool_call.get("function", {}).get("name")
                function_args = json.loads(
                    tool_call.get("function", {}).get("arguments", "{}")
                )

                logger.info(
                    f"Executing tool: {function_name} with args: {function_args}"
                )

                # Execute the tool
                result = self.tool_registry.execute_tool(function_name, **function_args)

                results.append(
                    {
                        "tool_call_id": tool_call.get("id"),
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result),
                    }
                )

            except Exception as e:
                logger.error(f"Tool execution failed: {str(e)}")
                results.append(
                    {
                        "tool_call_id": tool_call.get("id"),
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps({"success": False, "error": str(e)}),
                    }
                )

        return results

    def chat(self, message: str) -> AgentResponse:
        """
        Main chat method that handles the conversation flow.

        Args:
            message: User's message

        Returns:
            AgentResponse: The agent's response
        """
        start_time = time.time()
        iterations = 0
        tool_calls_made = []

        try:
            # Prepare initial messages
            messages = self._prepare_messages(message)

            # Main conversation loop
            while iterations < settings.max_iterations:
                iterations += 1

                # Check timeout
                if time.time() - start_time > settings.timeout_seconds:
                    raise TimeoutError(
                        f"Agent exceeded timeout of {settings.timeout_seconds} seconds"
                    )

                # Make API call
                response = self._make_api_call(messages)
                message_obj = response.choices[0].message

                # Check if the model wants to use tools
                if hasattr(message_obj, "tool_calls") and message_obj.tool_calls:
                    # Execute tool calls
                    tool_results = self._execute_tool_calls(message_obj.tool_calls)
                    tool_calls_made.extend(message_obj.tool_calls)

                    # Add assistant message and tool results to conversation
                    messages.append(
                        {
                            "role": "assistant",
                            "content": message_obj.content or "",
                            "tool_calls": message_obj.tool_calls,
                        }
                    )
                    messages.extend(tool_results)

                    # Continue the loop to get the final response
                    continue
                else:
                    # No tool calls, we have the final response
                    final_content = message_obj.content

                    # Add to conversation history
                    self.conversation_history.append(
                        Message(role="user", content=message)
                    )
                    self.conversation_history.append(
                        Message(role="assistant", content=final_content)
                    )

                    return AgentResponse(
                        content=final_content,
                        tool_calls_made=tool_calls_made,
                        iterations=iterations,
                        success=True,
                    )

            # If we reach here, we've exceeded max iterations
            raise RuntimeError(
                f"Agent exceeded maximum iterations ({settings.max_iterations})"
            )

        except Exception as e:
            logger.error(f"Chat failed: {str(e)}")
            return AgentResponse(
                content="I apologize, but I encountered an error while processing your request.",
                tool_calls_made=tool_calls_made,
                iterations=iterations,
                success=False,
                error=str(e),
            )

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history.clear()
        logger.info("Conversation history reset")

    def get_conversation_history(self) -> List[Message]:
        """Get the current conversation history."""
        return self.conversation_history.copy()

    def add_tool(self, tool):
        """Add a custom tool to the agent."""
        self.tool_registry.register_tool(tool)
        logger.info(f"Tool '{tool.name}' added to agent")
