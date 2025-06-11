from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .subagents.search_agent.agent import search_agent
from .subagents.greeting_agent.agent import greeting_agent
from .subagents.funny_nerd.agent import funny_nerd
from .subagents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time

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