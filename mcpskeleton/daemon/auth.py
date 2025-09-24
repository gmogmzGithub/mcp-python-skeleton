import logging

from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware

LOG = logging.getLogger(__name__)


class APIKeyMiddleware(BaseHTTPMiddleware):
    """Simple API key validation middleware for MCP routes."""

    def __init__(self, app, api_key: str):
        super().__init__(app)
        self.api_key = api_key

    async def dispatch(self, request: Request, call_next):
        # Only check API key for MCP routes
        if request.url.path.startswith("/mcp"):
            api_key = request.headers.get("X-API-Key")
            if not api_key or api_key != self.api_key:
                LOG.warning(f"Invalid API key for MCP route: {request.url.path}")
                return Response(
                    content="Invalid API key",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    headers={"WWW-Authenticate": "Bearer"},
                )

        return await call_next(request)
