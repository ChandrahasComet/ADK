from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from .tools import get_current_time, get_stock_price

# greeting agent

greeting_agent = Agent(
    name = "greeting_agent",
    model = "gemini-2.0-flash",
    description = "Greeting agent that greets the user",
    instruction = """
    You are a helpful AI assitant. Grret the user and ask him how you can help him.
    If you cant handle the query, delegate the request to the root agent.
    """
)

# funny_nerd agent
funny_nerd = Agent(
    name = "funny_nerd",
    model = "gemini-2.0-flash",
    description = "Funny nerd agent that gives jokes based on the given topic",
    instruction = """
    You are a helpful AI Based on the query provided, generate a funny joke about the metioned topic
    If you cant handle the query, delegate the request to the root agent.
    """
)

#search-agent
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

stock_analyst = Agent(
    name = "stock_analyst",
    model = "gemini-2.0-flash",
    description = "Stock analyst agent that can provide the stock price for the given ticker symbol",
    instruction = """
    You are a helpful AI assistant that can provide the stock price for the given ticker symbol.

    For the query you must first get the current time and then use the get_stock_price tool to get the stock price.

    Output format must be
    GOOG: $170.00 (2023-07-17 10:30:00)
    APPLE: $270.00 (2023-07-17 10:30:00)
""",
    tools = [get_stock_price]
)

root_agent = Agent(
    name = "manager",
    model = "gemini-2.0-flash",
    description = "Manager Agent",
    instruction = """
    You are a manager agent who is reponsible for overseeing the work of the other agents.

    Always delegate the task to the approapriate agent. User your best judgement to determine which agent to delegate to.

    You are responsible for delegating taks to the following agents:
    - greeting_agent
    - funny_nerd
    - stock_analyst

    You also have access to the following tools:
    - search_agent
    - get_current_time
""",
    sub_agents= [greeting_agent, funny_nerd, stock_analyst],
    tools = [AgentTool(search_agent), get_current_time] #sub agents cannot use tools so we need to pass the agent through the AgentTool class
)