import os
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from typing import *
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

load_dotenv()

conversation_history = []

def build_context_msg(user_msg: str) -> str:
    if not conversation_history:
        return user_msg
    
    recent_conversations = conversation_history[-2:] if len(conversation_history) >=2 else conversation_history

    context_message = ""
    if recent_conversations:
        context_message += "=== PREVIOUS CONVERSATION CONTEXT ===\n"
        for i, convo in enumerate(recent_conversations, 1):
            context_message += f"Previous Exchange {i}:\n"
            context_message += f"User: {convo['user']}\n"
            context_message += f"Assistant: {convo['agent']}\n\n"
        
        context_message += "=== END OF PREVIOUS CONTEXT ===\n\n"
    
    context_message += f"=== CURRENT USER MESSAGE ===\n{user_msg}"
    
    return context_message

def store_conversation(user_msg: str, agent_response: str) -> None:
    conversation_entry = {
        "user": user_msg,
        "agent": agent_response
    }
    conversation_history.append(conversation_entry)
    print(f" Stored conversation entry")

def get_conversation_history() -> List[Dict[str,str]]:
    """
    Retrieves the complete conversation history

    Args: 
        None

    Returns:
        List[Dict[str,str]]: A list of conversation dictionaries containing user and agent messages
    """
    return conversation_history.copy()

def clear_conversation_memory() -> None:
    global conversation_history
    conversation_history.clear()
    print("Conversation memory cleared.")

# --- Simplified Pydantic Models for a minimal API ---
# The incoming request only needs the user's message.
class ChatRequest(BaseModel):
    message: str

# The outgoing response only needs the agent's reply.
class ChatResponse(BaseModel):
    reply: str

async def get_agent():
    toolset = MCPToolset(
                connection_params= StdioServerParameters(
                    command = "/Library/Frameworks/Python.framework/Versions/3.11/bin/uv",
                    args = [
                        "run",
                        "--with",
                        "mcp[cli]",
                        "mcp",
                        "run",
                        "/Users/contenterra_m4512/Chandrahas/Projects/mcp_adk/mcp_servers/stock_price/stock_price.py"
                    ]
                )
            )
    
    agent = Agent(
        name = "stock_agent",
        model = "gemini-2.0-flash",
        instruction = """
        You are a stock analyst agent that fetches stock price for the requested company.
        Get the current stock price for a company using yfinance.
        The company_name should be the ticker symbol (e.g., 'AAPL' for Apple).

        You also have access to the conversation history through the get_conversation_history function.
        If a user asks about previous conversations or referes to something that was discussed earlier, use the get_conversation_history tool.

        IMPORTANT CONTEXT HANDLING:
        - You will receive messages that may include previous conversation history marked as "PREVIOUS CONVERSATION CONTEXT"
        - The actual user query will be marked as "CURRENT USER MESSAGE"
        - Use the previous context to understand references like "so what are their stock_prices", "so what about them"
        - If no previous context is provided, treat it as a fresh conversation

        Output format must be
        GOOG: $170.00 (2023-07-17 10:30:00)
        APPLE: $270.00 (2023-07-17 10:30:00)
""",
        tools = [toolset, get_conversation_history]
    )
    return agent, toolset

# --- FastAPI Lifespan for Startup/Shutdown ---
# This initializes the agent and runner ONCE when the server starts up.
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Server starting up...")
    print("🔧 Initializing Agent, Toolset, and Runner...")

    # clear any existing memomry on startup
    clear_conversation_memory()

    agent, toolset = await get_agent()
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="stock_api_app",
        agent=agent,
        session_service=session_service
    )
    
    # Store the initialized objects in the app's state
    app.state.runner = runner
    app.state.session_service = session_service
    app.state.toolset = toolset
    print("✅ Initialization complete. Server is ready.")

    yield  # The application is now running

    print("🌙 Server shutting down...")
    print("🔌 Closing MCP server connection...")
    await app.state.toolset.close()
    clear_conversation_memory()
    print("✅ Shutdown complete.")


# --- FastAPI Application ---
app = FastAPI(lifespan=lifespan)

# --- The Simplified API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat_handler(chat_request: ChatRequest, request: Request):
    """
    Handles a chat request. Each call is treated as a new, independent conversation.
    """
    runner = request.app.state.runner
    session_service = request.app.state.session_service

    # For simplicity, we create a new session for every single API call.
    # We use a static user_id because it's required by the ADK but not by our API.
    user_id_for_adk = "api_user"
    session = await session_service.create_session(user_id=user_id_for_adk, app_name="stock_api_app")

    try:
        context_message = build_context_msg(chat_request.message)
        content = types.Content(role='user', parts=[types.Part(text=context_message)])
        final_response_text = "Sorry, I could not generate a response."

        async with asyncio.timeout(60):
            async for event in runner.run_async(
                user_id=user_id_for_adk,
                session_id=session.id,
                new_message=content
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_response_text = event.content.parts[0].text.strip()
                    break

        # store the conversation in memory
        store_conversation(chat_request.message, final_response_text)

        return ChatResponse(reply=final_response_text)

    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"An internal server error occurred.")


# --- Main entry point to run the server ---
if __name__ == "__main__":
    uvicorn.run("api_agent:app", host="0.0.0.0", port=8080, reload=True)

