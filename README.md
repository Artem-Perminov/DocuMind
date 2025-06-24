# 🤖 AI Agent Template

A simple, extensible Python template for building AI agents using OpenAI-compatible APIs. This template provides a solid foundation for creating production-ready AI agents with tool integration, proper error handling, and comprehensive testing.

## ✨ Features

- **Simple Architecture**: Clean, modular design that's easy to understand and extend
- **Tool Integration**: Built-in support for custom tools (calculator, web search, etc.)
- **Error Handling**: Robust error handling and timeout management
- **Configuration Management**: Environment-based configuration with validation
- **Conversation Memory**: Maintains conversation history across interactions
- **Testing Suite**: Comprehensive unit tests and integration tests
- **Production Ready**: Proper logging, validation, and safety measures

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd docu_mind
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy the example environment file and add your API key:

```bash
cp env.example .env
```

Edit `.env` and set your OpenRouter API key:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 4. Run the Agent

```bash
python main.py
```

Choose from:
1. **Demo Mode**: See automated examples of the agent in action
2. **Interactive Chat**: Chat with the agent directly
3. **Exit**: Close the application

## 📁 Project Structure

```
docu_mind/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration management
├── src/
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── core.py          # Main AI Agent class
│   │   └── tools.py         # Tool implementations
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_agent.py        # Unit tests
├── main.py                  # Main demo script
├── requirements.txt         # Dependencies
├── env.example             # Environment template
└── README.md               # This file
```

## 🔧 Configuration

The agent is configured through environment variables. See `env.example` for all available options:

### API Configuration
- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `SITE_URL`: Your site URL for OpenRouter rankings
- `SITE_NAME`: Your site name for OpenRouter rankings

### Model Configuration
- `MODEL_NAME`: Model to use (default: `deepseek/deepseek-r1-0528:free`)
- `MAX_TOKENS`: Maximum tokens per response (default: 1000)
- `TEMPERATURE`: Response creativity (default: 0.7)

### Agent Configuration
- `MAX_ITERATIONS`: Maximum tool-use iterations (default: 10)
- `TIMEOUT_SECONDS`: Request timeout (default: 30)

## 🛠️ Using the Agent

### Basic Usage

```python
from src.agent import AIAgent

# Initialize the agent
agent = AIAgent()

# Chat with the agent
response = agent.chat("What is 25 * 4?")

if response.success:
    print(f"Agent: {response.content}")
    print(f"Used {len(response.tool_calls_made)} tools")
else:
    print(f"Error: {response.error}")
```

### Conversation Management

```python
# Get conversation history
history = agent.get_conversation_history()

# Reset conversation
agent.reset_conversation()
```

### Adding Custom Tools

```python
from src.agent.tools import Tool

class MyCustomTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="Description of what this tool does"
        )
    
    def get_parameters(self):
        return {
            "type": "object",
            "properties": {
                "input": {
                    "type": "string",
                    "description": "Input parameter description"
                }
            },
            "required": ["input"]
        }
    
    def execute(self, input: str):
        # Your tool logic here
        return {
            "success": True,
            "result": f"Processed: {input}"
        }

# Add to agent
agent.add_tool(MyCustomTool())
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Categories

- **Unit Tests**: Test individual components (models, tools, configuration)
- **Integration Tests**: Test agent functionality with actual API calls
- **Tool Tests**: Test tool execution and error handling

## 📋 Available Tools

### Calculator Tool
Performs basic mathematical calculations safely.

```python
# Usage example
response = agent.chat("What is 15 * 7 + 10?")
```

### Web Search Tool
Searches the web for information (currently returns mock data).

```python
# Usage example
response = agent.chat("Search for information about Python programming")
```

### Adding More Tools

1. Create a new tool class inheriting from `Tool`
2. Implement `get_parameters()` and `execute()` methods
3. Register it with the tool registry

## 🔒 Safety and Security

- **Input Validation**: All tool inputs are validated
- **Safe Execution**: Calculator tool prevents code injection
- **Error Handling**: Comprehensive error handling prevents crashes
- **Timeouts**: Configurable timeouts prevent infinite loops
- **Logging**: Detailed logging for debugging and monitoring

## 🎯 Use Cases

This template is perfect for:

- **Customer Support Bots**: Answer questions and help customers
- **Research Assistants**: Search and analyze information
- **Task Automation**: Automate repetitive tasks with tools
- **Educational Tools**: Interactive learning assistants
- **Prototype AI Applications**: Quick proof-of-concepts

## 🚧 Extending the Template

### Adding New Features

1. **Memory Systems**: Add persistent memory for long-term conversations
2. **Multi-Agent Support**: Create specialized agents for different tasks
3. **Advanced Tools**: Integrate with APIs, databases, or external services
4. **Web Interface**: Add FastAPI or Flask for web-based interaction
5. **Streaming Responses**: Implement real-time response streaming

### Recommended Libraries

For extending functionality:
- **LangChain**: Advanced agent frameworks
- **LangGraph**: Complex agent workflows
- **FastAPI**: Web API development
- **SQLAlchemy**: Database integration
- **Redis**: Caching and session management

## 🐛 Troubleshooting

### Common Issues

**API Key Not Found**
```
Error: OPENROUTER_API_KEY is not set or invalid
```
- Solution: Set your API key in the `.env` file

**Model Not Found**
```
Error: The model 'model-name' does not exist
```
- Solution: Check available models on OpenRouter and update `MODEL_NAME`

**Timeout Errors**
```
Error: Agent exceeded timeout of 30 seconds
```
- Solution: Increase `TIMEOUT_SECONDS` in your configuration

**Tool Execution Errors**
- Check tool implementation and input validation
- Review logs for detailed error information

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints for better code clarity
- Add docstrings for all public methods
- Keep functions focused and small

### Testing
- Write tests for all new features
- Maintain test coverage above 80%
- Test both success and failure scenarios
- Mock external API calls in unit tests

### Documentation
- Update README for new features
- Add inline comments for complex logic
- Document configuration options
- Provide usage examples

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section
2. Review the test cases for usage examples
3. Check logs for detailed error information
4. Create an issue with:
   - Your environment details
   - Steps to reproduce the problem
   - Expected vs actual behavior

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [OpenAI API](https://openai.com/)
- Uses [OpenRouter](https://openrouter.ai/) for model access
- Inspired by modern AI agent patterns and best practices

---

**Happy Building! 🚀** 