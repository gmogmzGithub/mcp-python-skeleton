"""
MCP tools for the skeleton server.

This module contains tool implementations to be exposed via the MCP server.
Add your custom tools here by defining functions and adding them to base_tools.
"""

import logging

LOG = logging.getLogger(__name__)


def get_mcp_tools(property_manager=None):
    """
    Function that returns a list of MCP tools.

    :param property_manager: Property manager instance from the webapp (optional)
    :return: List of tool functions
    """

    def echo(message: str) -> str:
        """
        Echo back the provided message.

        Args:
            message: The message to echo back

        Returns:
            The same message that was provided
        """
        return f"Echo: {message}"

    base_tools = [
        echo,
    ]

    return base_tools