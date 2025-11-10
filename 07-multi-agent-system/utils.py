import asyncio
from google.genai import types


async def process_user_input(runner, user_id, session_id, query):
    """Process a user query through the agent system."""
    print(f"\nYou: {query}")
    
    # Create content from the user query
    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    
    # Run the agent with the user query
    response = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    )

    # Process the response
    final_response_text = None
    
    async for event in response:
        if event.is_final_response():
            if event.content and event.content.parts:
                print("Final response:", event.content.parts[0].text)
                final_response_text = event.content.parts[0].text
                break

    # print(f"\nVacation Planner: {final_response_text}")
    return final_response_text


