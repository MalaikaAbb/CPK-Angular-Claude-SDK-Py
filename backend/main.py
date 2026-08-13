import logging
import os
from collections.abc import AsyncIterator

from ag_ui.core import EventType, RunAgentInput, RunErrorEvent
from ag_ui.encoder import EventEncoder
from ag_ui_claude_sdk import ClaudeAgentAdapter
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from claude_agent_sdk import tool, create_sdk_mcp_server
load_dotenv()
import json 

app = FastAPI(title="Claude Agent SDK Agent")
logger = logging.getLogger("claude_agent")

@tool("getWeather", "Get current weather for a location.", {"location": str})
async def getWeather(args: dict) -> dict:
    return {"content": [{"type": "text", "text": json.dumps({
        "city": args["location"],
        "temperature": 68,
        "humidity": 55,
        "wind_speed": 10,
        "conditions": "Sunny",
    })}]}


agent_tools_server = create_sdk_mcp_server(
    name="agent_tools", version="1.0.0", tools=[getWeather],
)


# Build the adapter once, at module scope. ClaudeAgentAdapter is a
# long-lived singleton that caches a worker (and its Claude SDK
# subprocess) per thread; constructing it per request would leak those
# workers and their subprocesses.
adapter = ClaudeAgentAdapter(
    name="claude_agent",
    options={
        "model": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6"),
        "system_prompt": "You are a helpful assistant embedded in a CopilotKit app.",
        "mcp_servers": {"agent_tools": agent_tools_server},
        "allowed_tools": [
            "mcp__agent_tools__getWeather"],
        "tools": [],
        "permission_mode": "dontAsk",
        "max_turns": 10,
    },
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/")
async def run_agent(request: Request) -> StreamingResponse:
    encoder = EventEncoder()

    input_data = RunAgentInput(**(await request.json()))

    async def event_stream() -> AsyncIterator[str]:
        try:
            async for event in adapter.run(input_data):
                yield encoder.encode(event)
        except Exception as error:
            # Every failure — malformed request body or streaming —
            # becomes a graceful RUN_ERROR, and the full detail is
            # logged server-side rather than only sent to the client.
            logger.exception("Claude agent run failed")
            yield encoder.encode(
                RunErrorEvent(
                    type=EventType.RUN_ERROR,
                    message=str(error),
                )
            )

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )