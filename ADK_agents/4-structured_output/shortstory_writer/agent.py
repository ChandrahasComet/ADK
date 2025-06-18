from google.adk.agents import LlmAgent
from .tools import get_stock_price
from pydantic import BaseModel, Field

class StoryBook(BaseModel): # the agent will give the in JSON format with the keys given in the class
    title: str = Field(
        description="The title of the short story"
    )
    story: str = Field(
        description="The short story"
    )

root_agent = LlmAgent(
    name = "shortstory_writer",
    model = "gemini-2.0-flash",
    description = "Short story writer agent",
    instruction = """
    You are a helpful AI assistant that can write short stories based on the user's request.
    Keep the stories small and sweet.
""",
    output_schema= StoryBook, # cant use tools when output schema is provided
    output_key= "shortstory_result"
)