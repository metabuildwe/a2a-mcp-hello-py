"""A2A Server for Hello MCP Agent."""

import os
import uvicorn  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()

from a2a.server.apps import A2AStarletteApplication  # type: ignore
from a2a.server.request_handlers import DefaultRequestHandler  # type: ignore
from a2a.server.tasks import InMemoryTaskStore  # type: ignore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill  # type: ignore

from agent_executor import HelloMCPAgentExecutor  # type: ignore


MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL",
    "https://mcp-hello-py-666155174404.asia-northeast3.run.app/mcp"
)


def create_agent_card(host: str, port: int) -> AgentCard:
    """Create the A2A Agent Card."""
    skill = AgentSkill(
        id="korean_greeting",
        name="Korean Greeting",
        description="이름을 받아 한국어로 인사합니다. MCP Hello Server를 사용합니다.",
        tags=["greeting", "korean", "mcp"],
        examples=[
            "김철수에게 인사해줘",
            "이영희, 박민수에게 인사해줘",
            "안녕하세요",
        ],
    )

    return AgentCard(
        name="Hello MCP Agent",
        description="MCP Hello Server를 사용하여 한국어로 인사하는 A2A 에이전트입니다.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        default_input_modes=["text"],
        default_output_modes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[skill],
    )


def main():
    """Main entry point."""
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 9999))

    agent_card = create_agent_card(host, port)

    request_handler = DefaultRequestHandler(
        agent_executor=HelloMCPAgentExecutor(MCP_SERVER_URL),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print(f"Starting A2A Hello MCP Agent on {host}:{port}")
    print(f"MCP Server URL: {MCP_SERVER_URL}")
    print(f"Agent Card URL: http://{host}:{port}/.well-known/agent.json")

    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    main()
