"""A2A Agent Executor for Hello MCP Agent."""

from a2a.server.agent_execution import AgentExecutor, RequestContext  # type: ignore
from a2a.server.events import EventQueue  # type: ignore
from a2a.server.tasks import TaskUpdater  # type: ignore
from a2a.types import Part, TaskState, TextPart  # type: ignore
from a2a.utils import new_agent_text_message, new_task  # type: ignore
from agent import HelloMCPAgent  # type: ignore


class HelloMCPAgentExecutor(AgentExecutor):
    """A2A Agent Executor that uses MCP Hello Server."""

    def __init__(self, mcp_url: str):
        self.agent = HelloMCPAgent(mcp_url)

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute the agent with user input."""
        user_message = ""
        if context.message and context.message.parts:
            for part in context.message.parts:
                if hasattr(part, 'text'):
                    user_message = part.text
                    break

        if not user_message:
            user_message = "친구"

        task = context.current_task or new_task(context.message)
        await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        try:
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(
                    "MCP 서버에 인사 요청 중...",
                    task.context_id,
                    task.id
                ),
            )

            result = await self.agent.invoke(user_message)

            await updater.add_artifact(
                [Part(root=TextPart(text=result))],
                name="greeting",
            )

            await updater.complete()

        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(
                    f"오류 발생: {str(e)}",
                    task.context_id,
                    task.id
                ),
                final=True,
            )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancel is not supported."""
        raise Exception("cancel not supported")
