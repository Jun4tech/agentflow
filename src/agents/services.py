from dataclasses import dataclass
from langgraph.graph.state import CompiledStateGraph
from collections.abc import AsyncGenerator
from agents.search_agent import web_agent

@dataclass
class Agent:
    description: str
    graph: CompiledStateGraph


agent_dict = {
    "search_agent": Agent(
        description="agent that searches info from the web",
        graph = web_agent
    )
}

def get_agent(agent_name: str) -> CompiledStateGraph:
    """
    Get agent by name
    """
    return agent_dict[agent_name].graph

async def get_stream_output(user_input: str, agent: CompiledStateGraph) -> AsyncGenerator[str, None]:
    """
    Get stream output from agent
    """
    async for event in agent.astream(
        {"messages": [{"role": "user", "content": user_input}]},
        stream_mode="updates"
        ):
        for value in event.values():
            yield f"Assistant: {value["messages"][-1].content}"
        
