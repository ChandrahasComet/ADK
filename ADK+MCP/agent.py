import os
import asyncio
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from dotenv import load_dotenv
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters


load_dotenv()

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

        Output format must be
        GOOG: $170.00 (2023-07-17 10:30:00)
        APPLE: $270.00 (2023-07-17 10:30:00)
""",
        tools = [toolset]
    )
    return agent, toolset

# async def get_rag_agent():
#     toolset = MCPToolset(
#                 connection_params= StdioServerParameters(
#                     command = "/Library/Frameworks/Python.framework/Versions/3.11/bin/uv",
#                     args = [
#                         "run",
#                         "--with",
#                         "mcp[cli]",
#                         "mcp",
#                         "run",
#                         "/Users/contenterra_m4512/Chandrahas/Projects/mcp_adk/mcp_servers/rag-server/rag_server.py"
#                     ],
#                     timeout = 30.0
#                 )
#             )
    
#     agent = Agent(
#         name = "rag_agent",
#         model = "gemini-2.0-flash",
#         instruction = """
#         You are a specialized RAG agent. Your sole purpose is to retrieve relevant contextual information from the vector database based on the user's query.

#         **Your Task:**
#         1.  Receive the user's original query.
#         2.  Use the `query_vector_store` tool with the user's query to fetch the most relevant context and get the answer.

#         Show the object returned from the tool to the user.


#         You can use the following tool:
#         - `query_vector_store`: Takes the user's query as input and returns a dictionary containing query and response keys.

#         ** Important Considerations: **
#         - When sending the user query to query_vector_store tool, do not minimise it. As the query will be used to retrieve documents from the vector database.
#         - minimising the user query might result in retrieval of irrelevant documents. So Strictly refrain from minimising the query.
#     """,
#         tools = [toolset]
#     )
#     return agent, toolset

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
                print("⚠️  Operation timed out. The RAG query is taking longer than expected.")
            except Exception as e:
                print(f"❌ Error during processing: {e}")

    finally:
        if toolset:
            print("Closing MCP server connection...")
            await toolset.close()

if __name__ == "__main__":
    asyncio.run(main())