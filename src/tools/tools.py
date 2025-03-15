from langchain_community.tools.tavily_search import TavilySearchResults

def toolbox():
    search_tool = TavilySearchResults(max_results=5)
    tools = [search_tool]
    return tools

