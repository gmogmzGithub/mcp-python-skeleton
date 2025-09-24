"""Main application implementation for the MCP skeleton."""

import logging

from mcpskeleton.daemon.fastapi_webapp import SimpleWebapp
from mcpskeleton.daemon.routes import non_api_router
from mcpskeleton.daemon.health_checks import create_health_router
from mcpskeleton.mcp import add_mcp_server_capabilities

LOG = logging.getLogger(__name__)


def build_app():
    """Build the FastAPI application."""
    # Create the FastAPI webapp
    webapp = SimpleWebapp("mcp-python-skeleton", port=8080)

    # Create the FastAPI app
    webapp.create_app()

    # Add basic routers
    webapp.app.include_router(non_api_router)
    webapp.app.include_router(create_health_router())


    # Add MCP server capabilities
    add_mcp_server_capabilities(webapp.app)

    return webapp.app