from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

# TBC postgressaver
from langgraph.checkpoint.memory import MemorySaver

from src.tools.search_tools import search_toolbox

from langchain_openai import ChatOpenAI

# from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.utils import secret_from_env

load_dotenv()
# TBC setup postgres for persistent storage
memory = MemorySaver()


class State(TypedDict):
    messages: Annotated[list, add_messages]


class SearchLLM:
    def __init__(self, model: str):
        self.model = model
        # TBC: Include multimodal functionality once ollama supports deepseek r1
        llm = ChatOpenAI(
            api_key=secret_from_env("OPENAI_API_KEY")(),
            model=model,
            temperature=0,
            timeout=None,
            streaming=True,
        )

        # llm = ChatOllama(model=model, temperature=0)
        # currently bind_tools is not support with deepseek.
        # https://github.com/ollama/ollama/issues/8517
        self.llm_with_tools = llm.bind_tools(search_toolbox())

    def chatbot(self, state: State):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)
# TBC: Include multimodal functionality
llm = SearchLLM("gpt-4o")
# llm = LLM("deepseek-r1:14B")
tool_node = ToolNode(tools=search_toolbox())
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", llm.chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
search_graph = graph_builder.compile(checkpointer=memory)
