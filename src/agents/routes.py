from typing import Optional
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from agents.schemas import UserInput
from agents.services import get_agent, get_stream_output

router = APIRouter(prefix="/api")


@router.post("/stream")
async def stream(
    input: UserInput, agent_name: Optional[str] = "data_analysis_agent"
) -> StreamingResponse:
    """
    Stream output of Agent
    """
    agent = get_agent(agent_name or "data_analysis_agent")

    return StreamingResponse(
        get_stream_output(input.message, agent), media_type="text/event-stream"
    )
