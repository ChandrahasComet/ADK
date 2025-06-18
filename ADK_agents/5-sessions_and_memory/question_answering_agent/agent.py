from google.adk.agents import Agent

question_answering_agent = Agent(
    name="question_answering_agent",
    model = "gemini-2.0-flash",
    description="A question answering agent that answers questions based on the provided context.",
    instruction = """
    You are a helpful AI assistant that answers questions about the user's preferences


    Here is some information about the user:
    Name : {user_name}
    Preferences: {user_preferences}
"""
)