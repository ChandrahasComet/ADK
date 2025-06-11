from google.adk.agents import Agent

greeting_agent = Agent(
    name = "greeting_agent",
    model = "gemini-2.0-flash",
    description = "Greeting agent that greets the user",
    instruction = """
    You are a helpful AI assitant. Grret the user and ask him how you can help him.
    If you cant handle the query, delegate the request to the root agent.
    """
)
