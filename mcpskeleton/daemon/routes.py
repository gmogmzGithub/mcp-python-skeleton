"""
Basic non-API routes for the MCP skeleton.

This module provides minimal routing functionality.
Extend as needed for your specific use case.
"""

import logging

import fastapi

LOG = logging.getLogger(__name__)

non_api_router = fastapi.APIRouter(tags=["basic"])


@non_api_router.get("/")
async def root():
    """Basic root endpoint."""
    return {"message": "MCP Python Skeleton Server", "status": "running"}