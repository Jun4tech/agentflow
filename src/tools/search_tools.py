from langchain_community.tools.tavily_search import TavilySearchResults


def search_toolbox():
    search_tool = TavilySearchResults(max_results=5)
    search_tools = [search_tool]
    return search_tools
