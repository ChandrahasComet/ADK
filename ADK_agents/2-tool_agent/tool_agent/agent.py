from google.adk.agents import Agent
from google.adk.tools import google_search
import datetime

def get_current_time(format: str)->dict:
    """
    Get the current time in the mentioned format.
    """
    return {
        "current_time": datetime.datetime.now().strftime(format) if format else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

root_agent = Agent(
    name = "tool_agent",
    model = "gemini-2.0-flash",
    description = "Search Agent",
    instruction = """
    You are a helpful AI assistant that uses the following tools
    If the time format is mentioned in the query, pass that as a parameter to the tool.
    If the format is not given, send and empty string
    Sometimes the format will be mentioned like this : DD-MM-YYYY HH:MM:SS. In that case you have to convert Day to %d, Month to %m, Year to %Y, Hour to %H, Minute to %M, Second to %S. The combine them in the required format and send as the parameter to the tool.
    -get_current_time.
""",
    tools = [get_current_time]
)
