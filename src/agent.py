"""A2A Agent that uses MCP Hello Server."""

import re
from mcp_client import MCPHelloClient  # type: ignore


class HelloMCPAgent:
    """Agent that greets users using MCP Hello Server."""

    def __init__(self, mcp_url: str):
        self.mcp_client = MCPHelloClient(mcp_url)

    async def invoke(self, user_message: str) -> str:
        """Process user message and return greeting."""
        message_lower = user_message.lower()

        names = self._extract_names(user_message)

        if len(names) > 1:
            return await self.mcp_client.say_hello_multiple(names)
        elif len(names) == 1:
            return await self.mcp_client.say_hello(names[0])
        elif "안녕" in message_lower or "hello" in message_lower or "hi" in message_lower:
            return await self.mcp_client.say_hello("친구")
        else:
            return await self.mcp_client.say_hello(user_message.strip())

    def _extract_names(self, message: str) -> list[str]:
        """Extract names from the message."""
        patterns = [
            r"(\w+)(?:에게|한테|님께)",
            r"(\w+)(?:,\s*|\s+and\s+|\s+그리고\s+)",
            r"인사해\s*줘?\s*(.+)",
        ]

        names = []
        for pattern in patterns:
            matches = re.findall(pattern, message)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        names.extend([n.strip() for n in match if n.strip()])
                    else:
                        potential_names = re.split(r'[,\s]+(?:and|그리고)?\s*', match)
                        names.extend([n.strip() for n in potential_names if n.strip()])

        return list(dict.fromkeys(names)) if names else []
