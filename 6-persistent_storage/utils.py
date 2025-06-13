from google.genai import types
import asyncio



async def call_agent(runner, user_id,session_id,query):
    new_message = types.Content(role = 'user', parts = [types.Part(text=query)])
    final_response_text = None

    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            #process each event and get the final response
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text.strip()
                    print(
                    f"╔══ AGENT RESPONSE ═════════════════════════════════════════\n"
                    )
                    print(f"{final_response}")
                    print(
                    f"╚═════════════════════════════════════════════════════════════\n"
                    )

    except Exception as e:
        print(f"Error during agent call: {e}")
    
    return final_response_text