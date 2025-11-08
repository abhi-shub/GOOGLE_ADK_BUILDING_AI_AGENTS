import asyncio
# from google.generativeai.types import content_types
# from google.generativeai.types.content_types import Part

from google.genai import types


async def call_agent_async(runner, app_name,  user_id, session_id, query):
    """Process a user query through the agent asynchronously."""
    print(f"\nUser: {query}")
    
    # Create content from the user query
    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    
    # Get the session to see state before processing
    session = await runner.session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"\nState before processing: {session.state}")
    
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
    
    # Get updated session to see state after processing
    session = await runner.session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"\nState after processing: {session.state}")
    
    print(f"\nAgent: {final_response_text}")
    return final_response_text