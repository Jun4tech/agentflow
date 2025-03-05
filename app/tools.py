import json
from langchain_core.messages import ToolMessage
from langchain_community.tools.tavily_search import TavilySearchResults

def toolbox():
    search_tool = TavilySearchResults(max_results=3)
    tools = [search_tool]
    return tools

