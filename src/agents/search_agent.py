from dotenv import load_dotenv
import os
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages

#memory saver
from tools.tools import toolbox

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

class State(TypedDict):
    messages: Annotated[list, add_messages]

class LLM:
    def __init__(self, model: str):
        self.model = model
        api_key = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0,
            max_tokens=None,
            timeout=None
        )
        self.llm_with_tools = llm.bind_tools(toolbox())

    def chatbot(self, state: State):
        return {"messages": [self.llm_with_tools.invoke(state["messages"])]}

graph_builder = StateGraph(State)
llm = LLM('gpt-4o')
tool_node = ToolNode(tools= toolbox())
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", llm.chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
web_agent = graph_builder.compile()