from google.adk.agents import Agent
from google.adk.tools import google_search

search_agent = Agent(
    name = "search_agent",
    model = "gemini-2.0-flash",
    description = "Search agent that searches the web for the given query",
    instruction = """
    You are a helpful AI assistant that searches the web for the given query. You can use the google_search tool to search the web."
    If you cant handle the query, delegate the request to the root agent.
    """,
    tools = [google_search]
)