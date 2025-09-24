import logging
from typing import Callable

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

from mcpskeleton.mcp.mcp_tools import get_mcp_tools

LOG = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    "mcpskeleton-server", streamable_http_path="/", stateless_http=True
)  # noqa: F811


def register_tool(func: Callable) -> None:
    """Register a tool function with the MCP server."""
    mcp.tool()(func)
    LOG.info(f"Registered tool: {func.__name__}")


def _initialize_mcp_server(property_manager=None):
    """Initialize the MCP server with all tools registered."""
    # Register all tools before the server starts handling requests
    tools = get_mcp_tools(property_manager=property_manager)
    for tool in tools:
        register_tool(tool)
    LOG.info(f"Initialized MCP server with {len(tools)} tools")
    # Log SSE deprecation warning at startup
    LOG.warn("⚠️  SSE TRANSPORT DEPRECATION WARNING ⚠️")
    LOG.warn(
        "The Server-Sent Events (SSE) transport has been officially DEPRECATED. Please use Streamable HTTP instead."
    )
    LOG.warn(
        "SSE connections may drop intermittently and are not suitable for production use."
    )

    # Log SSE deprecation warning at startup
    LOG.warning("⚠️  SSE TRANSPORT DEPRECATION WARNING ⚠️")
    LOG.warning(
        "The Server-Sent Events (SSE) transport has been officially DEPRECATED. Please use Streamable HTTP instead."
    )
    LOG.warning(
        "SSE connections may drop intermittently and are not suitable for production use."
    )


def add_mcp_server_capabilities(app: FastAPI):
    """Add MCP server support with streamable HTTP transport"""
    # Initialize MCP server with tools BEFORE mounting
    # Pass the app's property manager to the tools
    property_manager = getattr(app, "pm", None)
    _initialize_mcp_server(property_manager=property_manager)

    app.mount("/mcp", mcp.streamable_http_app())

    # Use the existing MCP server instance
    app.mcp = mcp

    # Add testing endpoints (for development/debugging only)
    _add_testing_endpoints(app)


def _add_testing_endpoints(app: FastAPI):
    """Add custom testing endpoints (NOT for MCP client consumption)."""

    @app.get("/info", tags=["MCP"], include_in_schema=True)
    async def mcp_info():
        """
        Get information about available MCP tools and capabilities using the official MCP SDK
        NOTE: This is a testing endpoint only. MCP clients should use the /mcp endpoint with MCP protocol.
        """
        # Get server information from the MCP instance
        server_info = {
            "server_name": app.mcp.name,
            "description": f"MCP server '{app.mcp.name}' with dynamic capabilities",
            "transport": "streamable-http",
            "endpoints": {"mcp": "/mcp"},
            "note": "This is a testing endpoint. Use /mcp for MCP protocol communication.",
        }

        # Initialize capabilities
        capabilities = {"tools": False, "resources": False, "prompts": False}

        # Try to get tools using the FastMCP instance directly
        try:
            tools_list = await app.mcp.list_tools()
            capabilities["tools"] = True

            # Format tools information
            tools_info = []
            for tool in tools_list:
                tool_desc = f"{tool.name}("
                if (
                    hasattr(tool, "inputSchema")
                    and tool.inputSchema
                    and "properties" in tool.inputSchema
                ):
                    # Extract parameter information from the schema
                    properties = tool.inputSchema["properties"]
                    params = []
                    for param_name, param_info in properties.items():
                        param_type = param_info.get("type", "any")
                        params.append(f"{param_name}: {param_type}")
                    tool_desc += ", ".join(params)
                tool_desc += f") - {tool.description or 'No description available'}"
                tools_info.append(tool_desc)

            server_info["available_tools"] = tools_info
            server_info["total_tools"] = len(tools_info)

        except (AttributeError, RuntimeError, TypeError, ValueError) as e:
            server_info["available_tools"] = []
            server_info["total_tools"] = 0
            server_info["tools_note"] = (
                f"Could not retrieve tools dynamically: {str(e)}"
            )

        # Try to get resources
        try:
            resources_list = await app.mcp.list_resources()
            capabilities["resources"] = True
            server_info["available_resources"] = [
                f"{resource.uri} - {resource.name}" for resource in resources_list
            ]
        except (AttributeError, RuntimeError, TypeError, NotImplementedError):
            capabilities["resources"] = False
            server_info["available_resources"] = []

        # Try to get prompts
        try:
            prompts_list = await app.mcp.list_prompts()
            capabilities["prompts"] = True
            server_info["available_prompts"] = [
                f"{prompt.name} - {prompt.description or 'No description'}"
                for prompt in prompts_list
            ]
        except (AttributeError, RuntimeError, TypeError, NotImplementedError):
            capabilities["prompts"] = False
            server_info["available_prompts"] = []

        server_info["capabilities"] = capabilities

        return server_info
