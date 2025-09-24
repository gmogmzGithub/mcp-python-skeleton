# MCP Python Skeleton

A skeleton/template for building [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers in Python using FastAPI.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI applications to securely access external data and tools. MCP servers provide a standardized way to expose capabilities to AI models.

## Features

- **FastAPI-based**: Modern, fast web framework with automatic API documentation
- **MCP Integration**: Built-in support for MCP protocol using FastMCP
- **Simple Architecture**: Clean, extensible codebase that's easy to understand and modify
- **Health Checks**: Built-in health check endpoints for monitoring
- **Docker Support**: Ready-to-deploy Docker configuration
- **Testing Setup**: Pre-configured testing with pytest and tox
- **Code Quality**: Pre-commit hooks for formatting and linting

## Getting Started

### Prerequisites

- Python 3.12+
- Poetry (for dependency management)

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/mcp-python-skeleton.git
   cd mcp-python-skeleton
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

   **Note**: The `poetry.lock` file is intentionally ignored in git. Poetry will generate a fresh lock file when you run `poetry install` for the first time.

3. Install pre-commit hooks (optional but recommended):
   ```bash
   poetry run pre-commit install
   ```

### Running the Server

#### Option 1: Using Poetry
```bash
# Run with default settings
poetry run python -m mcpskeleton

# Run with custom port
PORT0=9000 poetry run python -m mcpskeleton

# Run in debug mode
poetry run python -m mcpskeleton --debug
```

#### Option 2: Using Poetry Script
```bash
poetry run start
```

The server will start at `http://0.0.0.0:8080` by default.

### Available Endpoints

- `GET /health` - Basic health check
- `GET /` - Root endpoint (JSON response)
- `/mcp/*` - MCP protocol endpoints

## Adding MCP Tools

MCP tools are defined in `mcpskeleton/mcp/mcp_tools.py`. Here's how to add a new tool:

```python
def my_custom_tool(param1: str, param2: int) -> str:
    """
    Description of what this tool does.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value
    """
    return f"Processed {param1} with value {param2}"

# Add your tool to the base_tools list
base_tools = [
    my_custom_tool,  # Add your function here
]
```

**Important Notes:**
- Always include type hints for parameters and return values
- Add comprehensive docstrings - they help the LLM understand how to use your tools
- The function name will be used as the tool name in the MCP protocol

## Configuration

### Environment Variables

- `PORT0`: Server port (default: 8080)
- `HOST0`: Server host (default: 0.0.0.0)
- `WORKERS`: Number of worker processes (default: 1)


## Development

### Running Tests

```bash
# Run all tests with coverage
poetry run tox

# Run tests only (no linting)
poetry run pytest

# Run specific test file
poetry run pytest mcpskeleton/tests/test_specific.py
```

### Code Quality

This project uses pre-commit hooks for code formatting and linting:

```bash
# Run all hooks manually
poetry run pre-commit run --all-files

# Auto-format code
poetry run black .
poetry run isort .

# Run linting
poetry run flake8
```

### Project Structure

```
mcpskeleton/
├── __main__.py              # Application entry point
├── daemon/                  # Web server components
│   ├── fastapi_webapp.py   # FastAPI application setup
│   ├── implementation.py   # Main app factory
│   ├── routes.py           # Basic routes
│   ├── health_checks.py    # Health check endpoints
│   └── dependencies.py     # Simple dependency management
├── mcp/                    # MCP-specific components
│   ├── __init__.py         # MCP server setup
│   └── mcp_tools.py        # MCP tool definitions
└── tests/                  # Basic test files
```

## Customization

### Adding Dependencies

Add your dependencies to `pyproject.toml`:

```toml
[tool.poetry.dependencies]
requests = "^2.31.0"
my-package = "^1.0.0"
```

Then run `poetry lock` to update the lock file.

### Adding Health Checks

Extend the simple health check in `mcpskeleton/daemon/dependencies.py`:

```python
def check_dependencies():
    """Add your custom dependency checks here."""
    # Example: check database connection, external APIs, etc.
    return {"status": "healthy", "dependencies": ["service1", "service2"]}
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `poetry run tox`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)

## Support

If you encounter any issues or have questions, please:

1. Check the [existing issues](https://github.com/your-username/mcp-python-skeleton/issues)
2. Create a new issue with detailed information about your problem
3. Include steps to reproduce, expected behavior, and actual behavior