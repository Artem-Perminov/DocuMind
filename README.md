# docu_mind

A collection of AI agents and tools built with Python. Each agent is organized in its own subdirectory under `/projects/`, making it easy to explore and run different AI implementations.

A Python project using the blazing-fast [uv package manager](https://docs.astral.sh/uv/) for dependency management.

## Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd docu_mind
```

### 2. Install uv package manager

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 3. Verify uv installation
```bash
uv --version
```

### 4. Install the latest Python version
```bash
uv python install
```

### 5. Check installed Python versions
```bash
uv python list --only-installed
```

### 6. Install project dependencies
```bash
uv sync
```

### 7. Setup environment variables
Create a `.env` file in the project root:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Development Commands

```bash
# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Remove dependency
uv remove package-name

# List installed packages
uv pip list

# Check Python version in uv environment
uv run python --version

# Run script with uv
uv run script.py

# Update dependencies
uv sync
```

## Running AI Agents

To run any agent from the project root:

```bash
# Example: Run the simple chatbot
uv run python projects/simple-bot/code.py
```

## Why uv?

- **⚡ 10-100x faster** than pip
- **🔧 Drop-in replacement** for pip, pip-tools, and virtualenv
- **🚀 Built with Rust** for maximum performance
- **📦 Better dependency resolution** and conflict handling 