from langchain_community.tools import DuckDuckGoSearchRun

search_tool=DuckDuckGoSearchRun()

res=search_tool.invoke("top service based companies name india?")

print(res)


"""
duckduckgo_search
A wrapper around DuckDuckGo Search. 
Useful for when you need to answer questions about 
current events. Input should be a search query.

{
    'query': 
            {
                'description': 'search query to look up', 
                'title': 'Query', 
                'type': 'string'
            }
}
"""