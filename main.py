#!/usr/bin/env python3
"""
Main script to demonstrate the AI Agent functionality.
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from agent import AIAgent
from config import settings


def demo_basic_chat():
    """Demonstrate basic chat functionality."""
    print("=== Basic Chat Demo ===")

    try:
        # Initialize agent
        agent = AIAgent()

        # Test basic conversation
        questions = [
            "Hello! What can you help me with?",
            "What is 25 * 4?",
            "Can you search for information about Python programming?",
        ]

        for question in questions:
            print(f"\n👤 User: {question}")
            response = agent.chat(question)

            if response.success:
                print(f"🤖 Agent: {response.content}")
                if response.tool_calls_made:
                    print(
                        f"🔧 Tools used: {len(response.tool_calls_made)} tool call(s)"
                    )
                print(f"⚡ Completed in {response.iterations} iteration(s)")
            else:
                print(f"❌ Error: {response.error}")

    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure you have set your OPENROUTER_API_KEY in a .env file")


def interactive_chat():
    """Start an interactive chat session."""
    print("=== Interactive Chat Session ===")
    print("Type 'quit', 'exit', or 'bye' to end the session")
    print("Type 'reset' to clear conversation history")
    print("Type 'history' to see conversation history")
    print("-" * 50)

    try:
        agent = AIAgent()

        while True:
            try:
                user_input = input("\n👤 You: ").strip()

                if user_input.lower() in ["quit", "exit", "bye"]:
                    print("👋 Goodbye!")
                    break

                if user_input.lower() == "reset":
                    agent.reset_conversation()
                    print("🔄 Conversation history cleared!")
                    continue

                if user_input.lower() == "history":
                    history = agent.get_conversation_history()
                    if history:
                        print("📜 Conversation History:")
                        for i, msg in enumerate(history, 1):
                            print(
                                f"  {i}. {msg.role}: {msg.content[:100]}{'...' if len(msg.content) > 100 else ''}"
                            )
                    else:
                        print("📜 No conversation history yet")
                    continue

                if not user_input:
                    print("Please enter a message or 'quit' to exit.")
                    continue

                print("🤖 Thinking...")
                response = agent.chat(user_input)

                if response.success:
                    print(f"🤖 Agent: {response.content}")
                    if response.tool_calls_made:
                        print(
                            f"🔧 (Used {len(response.tool_calls_made)} tool(s) in {response.iterations} iteration(s))"
                        )
                else:
                    print(f"❌ Error: {response.error}")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {str(e)}")

    except Exception as e:
        print(f"❌ Failed to start interactive chat: {str(e)}")
        print("Make sure you have set your OPENROUTER_API_KEY in a .env file")


def test_configuration():
    """Test configuration and API key setup."""
    print("=== Configuration Test ===")

    print(f"Model: {settings.model_name}")
    print(f"Max Tokens: {settings.max_tokens}")
    print(f"Temperature: {settings.temperature}")
    print(f"Debug Mode: {settings.debug}")

    if settings.validate_api_key():
        print("✅ API key is configured")
    else:
        print("❌ API key is not configured properly")
        print("Please set OPENROUTER_API_KEY in your .env file")
        return False

    return True


def main():
    """Main function."""
    print("🚀 AI Agent Template")
    print("=" * 30)

    # Test configuration first
    if not test_configuration():
        return

    print("\nChoose an option:")
    print("1. Run demo (automated test)")
    print("2. Interactive chat")
    print("3. Exit")

    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                demo_basic_chat()
                break
            elif choice == "2":
                interactive_chat()
                break
            elif choice == "3":
                print("👋 Goodbye!")
                break
            else:
                print("Please enter 1, 2, or 3")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break


if __name__ == "__main__":
    main()
