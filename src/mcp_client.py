"""MCP Client for calling MCP Hello Server."""

from mcp import ClientSession  # type: ignore
from mcp.client.streamable_http import streamablehttp_client  # type: ignore


class MCPHelloClient:
    """Client to interact with MCP Hello Server."""

    def __init__(self, mcp_url: str):
        self.mcp_url = mcp_url

    async def say_hello(self, name: str) -> str:
        """Call the say_hello tool on MCP server."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "say_hello",
                    arguments={"name": name}
                )

                if result.content and len(result.content) > 0:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        return content.text
                return "인사를 받지 못했습니다."

    async def say_hello_multiple(self, names: list[str]) -> str:
        """Call the say_hello_multiple tool on MCP server."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                result = await session.call_tool(
                    "say_hello_multiple",
                    arguments={"names": names}
                )

                if result.content and len(result.content) > 0:
                    content = result.content[0]
                    if hasattr(content, 'text'):
                        return content.text
                return "인사를 받지 못했습니다."

    async def list_tools(self) -> list[dict]:
        """List available tools from MCP server."""
        async with streamablehttp_client(self.mcp_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()

                tools = await session.list_tools()
                return [
                    {
                        "name": tool.name,
                        "description": tool.description
                    }
                    for tool in tools.tools
                ]
