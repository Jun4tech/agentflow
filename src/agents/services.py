from dataclasses import dataclass
from langgraph.graph.state import CompiledStateGraph
from collections.abc import AsyncGenerator
from agents.search_agent import search_graph
from agents.data_analysis_agent import data_analysis_graph
from agents.utils import langchain_to_chat_message
import json


@dataclass
class Agent:
    description: str
    graph: CompiledStateGraph


agent_dict = {
    "search_agent": Agent(
        description="agent that searches info from the web", graph=search_graph
    ),
    "data_analysis_agent": Agent(
        description="agent that analyzes data", graph=data_analysis_graph
    ),
}


def get_agent(agent_name: str) -> CompiledStateGraph:
    """
    Get agent by name
    """
    return agent_dict[agent_name].graph


# TBC: enchance to maintain state message
async def get_stream_output(
    user_input: str, agent: CompiledStateGraph
) -> AsyncGenerator[str, None]:
    """
    Get stream output from agent
    """

    async for event in agent.astream(
        {"messages": [{"role": "user", "content": user_input}]},
        # TBC: to be replaced with a more generic way to get the thread id
        {"configurable": {"thread_id": "1"}},
        stream_mode="updates",
    ):
        for value in event.values():
            if "messages" in value and value["messages"]:
                output = langchain_to_chat_message(value["messages"][-1])

                if output.type == "ai" and len(output.tool_calls) > 0:
                    yield f"data: {json.dumps({'type': 'web_search', 'content': 'Let me find information from the web...'})}\n\n"
                elif output.type == "tool":
                    yield f"data: {json.dumps({'type': 'web_result', 'content': f'{output.content}'})}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'agent_response', 'content': f'{output.content}'})}\n\n"
            else:
                pass
