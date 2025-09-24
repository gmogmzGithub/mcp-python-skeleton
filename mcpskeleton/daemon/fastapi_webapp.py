"""Simple FastAPI webapp for MCP server."""

from contextlib import AsyncExitStack, asynccontextmanager
import logging
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from mcpskeleton.mcp import mcp

log = logging.getLogger(__name__)


class HealthCheck(BaseModel):
    status: str


class SimpleWebapp:
    """Simple FastAPI webapp for MCP server."""

    def __init__(self, app_name: str = "mcp-python-skeleton", port: int = 8080):
        self.name = app_name
        self._port = port
        self.app: Optional[FastAPI] = None

    @property
    def port(self):
        return self._port

    def _create_lifespan(self):
        """Create the lifespan context manager for FastAPI application lifecycle."""

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            async with AsyncExitStack() as stack:
                # Start MCP session manager
                await stack.enter_async_context(mcp.session_manager.run())
                yield

        return lifespan

    def create_app(self) -> FastAPI:
        """Create and configure the FastAPI application with lifespan events."""
        app = FastAPI(
            title=self.name,
            description="MCP Python Skeleton Server",
            version="0.1.0",
            lifespan=self._create_lifespan()
        )

        # Add basic health check endpoint
        @app.get("/health", response_model=HealthCheck)
        async def health_check():
            return {"status": "healthy"}

        self.app = app
        return app