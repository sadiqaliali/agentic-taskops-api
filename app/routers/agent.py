import asyncio
import json
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from app.core.dependencies import get_current_active_user
from app.models.user import User

# Why: Grouping this router's endpoints under an "Agent" tag in the API docs.
router = APIRouter(tags=["Agent"])

class AgentRunRequest(BaseModel):
    """Schema for the request body of the agent execution endpoint."""
    prompt: str
    
# Why: A Server-Sent Events (SSE) endpoint is crucial for agentic applications.
# It allows the server to push updates to the client in real-time as the agent
# "thinks" or executes a long-running task. This provides a much better user
# experience than a long-polling request.
async def fake_agent_response_generator(prompt: str, user: User):
    """
    An async generator that simulates a long-running agent task,
    yielding formatted SSE messages.
    """
    # Event: Task Begin
    # Why: Send a structured event to the client indicating the task has started.
    # A client could use the 'event' field to trigger specific UI updates.
    yield f"event: task_start\ndata: {json.dumps({'message': 'Agent task execution started...'})}\n\n"
    await asyncio.sleep(1)

    # Event: Message Stream
    # Why: Stream back the response word by word to simulate token generation.
    response = f"Simulating execution for prompt: '{prompt}' on behalf of user '{user.email}'. "
    for word in response.split():
        yield f"data: {json.dumps({'token': word})}\n\n"
        await asyncio.sleep(0.1)

    await asyncio.sleep(1)

    # Event: Task End
    # Why: Signal to the client that the task is complete.
    yield f"event: task_end\ndata: {json.dumps({'message': 'Task completed successfully!'})}\n\n"

@router.post("/run", status_code=status.HTTP_200_OK)
async def agent_run(
    request: AgentRunRequest,
    current_user: User = Depends(get_current_active_user),
):
    """
    Run an agent task and stream the response back using Server-Sent Events.
    """
    # Why: We return a StreamingResponse, which FastAPI handles specially.
    # It takes an async generator (like ours) and streams its output to the client.
    # The 'text/event-stream' media type is the standard for SSE.
    return StreamingResponse(
        fake_agent_response_generator(request.prompt, current_user),
        media_type="text/event-stream"
    )
