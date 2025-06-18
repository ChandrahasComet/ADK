"""
This script must outside of the agent directory 

"""
from dotenv import load_dotenv
from google.adk.runners import Runner    
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid
from question_answering_agent import question_answering_agent
import asyncio

load_dotenv()

async def main():
    #create a new session
    session_service = InMemorySessionService()

    initial_state = {
        "user_name": "Chandrahas",
        "user_preferences":"""
        I like creating new agents for simplifying my workflow.
        I like playing a lot of video games during my free time.
        I am 21 years old.
    """
    }

    APP_NAME = "Chandrahas Bot"
    USER_ID = "chandrahas_1606"
    SESSION_ID = str(uuid.uuid4())

    stateful_session = await session_service.create_session(
        session_id=SESSION_ID,
        user_id=USER_ID,
        app_name=APP_NAME,
        state=initial_state
    )
    print(f"\t\tSession ID: {SESSION_ID}")

    # Create a Runner

    runner = Runner(
        agent = question_answering_agent,
        session_service= session_service,
        app_name = APP_NAME
    )

    # this is how you would want to send the message to the agents in your app, as we cant use ADK web in there
    new_message = types.Content(
        role = 'user', parts = [types.Part(text = "What is chandrahas's favorite thing to do?")]
    )



    # For the given user_id and the session_id we will run the new_message throught the agent
    for event in runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=new_message
    ):
        # the runner go through all the available agents,tools, select the approapriate one and send all the context to that agent
        if event.is_final_response():
            if event.content and event.content.parts:
                print(f" Final Response: {event.content.parts[0].text}")


    print("=== Session Exploration ===")
    session =await session_service.get_session(session_id=SESSION_ID, app_name=APP_NAME, user_id=USER_ID)
    # Log final session state
    print("=== Final Session State===")
    for key, value in session.state.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())

