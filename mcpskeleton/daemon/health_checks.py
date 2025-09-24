"""Simple health check endpoints for the MCP server."""

from fastapi import APIRouter
from pydantic import BaseModel

from .dependencies import get_health_status


class HealthStatus(BaseModel):
    """Health status response model."""
    status: str


def create_health_router() -> APIRouter:
    """Create router with basic health check endpoint."""
    router = APIRouter(prefix="/health", tags=["health"])

    @router.get("/", response_model=HealthStatus)
    async def health_check():
        """Basic health check endpoint."""
        health = get_health_status()
        return HealthStatus(status=health["status"])

    return router