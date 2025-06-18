from remainder_agent import remainder_agent
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types
from utils import call_agent
import uuid
import asyncio

load_dotenv()
# Initialize persistent session service

db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# Define an inirial state. This will only be used when creating a new session
initial_state = {
    "user_name": "Chandrahas",
    "user_remainders": []
}

async def main():
    APP_NAME = "Remainder Agent"
    USER_ID = "chandrahas_1606"

    # Find existing sessions
    existing_sessions = await session_service.list_sessions(
        user_id=USER_ID,
        app_name=APP_NAME
    )

    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing session {SESSION_ID}")
    
    else:
        # create a new session with initial state
        new_session = await session_service.create_session(
            user_id=USER_ID,
            app_name=APP_NAME,
            state=initial_state
        )
        SESSION_ID = new_session.id
        print(f"Created new session {SESSION_ID}")

    
    # Runner Setup

    runner = Runner(
        agent = remainder_agent,
        session_service= session_service,
        app_name = APP_NAME
    )

    print("Type 'exit' or 'quit' to end the conversation.")

    while True:
        # Get user input
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Ending Convo. Your data has been saved to the database.")
            break

        # process the user query through the agent
        await call_agent(runner, USER_ID, SESSION_ID, user_input)


if __name__ == "__main__":
    asyncio.run(main())