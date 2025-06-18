import os
import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.models.lite_llm import LiteLlm # Import this litellm wrapper to use the local ollama model in your agent


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
        model = LiteLlm(model = "ollama_chat/qwen3"),
        instruction = """
        /set nothink
        You are a stock analyst agent that fetches stock price for the requested company.
        Get the current stock price for a company using yfinance.
        The company_name should be the ticker symbol (e.g., 'AAPL' for Apple).

        Output format must be
        GOOG: $170.00 (2023-07-17 10:30:00)
        APPLE: $270.00 (2023-07-17 10:30:00)
""", # Disable thinking(only for models that support it) for quicker responses
        tools = [toolset]
    )
    return agent, toolset

async def main():
    try:
        agent, toolset = await get_agent()

        session_service = InMemorySessionService()
        session =  await session_service.create_session(
            state = {},
            app_name = "test",
            user_id = "chandrahas"
        )

        runner = Runner(
            app_name="test",
            agent=agent,
            session_service=session_service
        )

        while True:
            user_input = input("You: ")

            if user_input.lower() in ['exit', 'quit']:
                print("Ending Convo. Bye!")
                break

            content = types.Content(role = 'user', parts = [types.Part(text = user_input)])

            try:
                # Add timeout handling at the runner level too
                async with asyncio.timeout(60):  # 60 second timeout for the entire operation
                    async for event in runner.run_async(
                        user_id="chandrahas",
                        session_id=session.id,
                        new_message=content
                    ):
                        if event.is_final_response():
                            if event.content and event.content.parts:
                                final_response = event.content.parts[0].text.strip()
                                print(
                                    f"╔══ AGENT RESPONSE ═════════════════════════════════════════\n"
                                    f"║ {final_response}\n"
                                    f"╚══════════════════════════════════════════════════════════\n"
                                )
            except asyncio.TimeoutError:
                print("⚠️  Operation timed out. The query is taking longer than expected.")
            except Exception as e:
                print(f"❌ Error during processing: {e}")

    finally:
        if toolset:
            print("Closing MCP server connection...")
            await toolset.close()

if __name__ == "__main__":
    asyncio.run(main())