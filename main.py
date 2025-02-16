import os
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

class State(TypedDict):
    messages: Annotated[list, add_messages]

#tbc to include to separate file
class LLM:
    def __init__(self, model: str):
        self.model = model
        api_key = os.environ["OPENAI_API_KEY"]
        self.llm = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0,
            max_tokens=None,
            timeout=None
        )

    def chatbot(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}

def stream_graph_updates(user_input: str, graph):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)

def main():
    graph_builder = StateGraph(State)
    llm = LLM('gpt-4o')
    graph_builder.add_node("chatbot", llm.chatbot)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile()

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            stream_graph_updates(user_input, graph)
        except:
            # fallback if input() is not available
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            stream_graph_updates(user_input)
            break




if __name__ == "__main__":
    main()
