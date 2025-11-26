import os
import asyncio
import uuid
from dotenv import load_dotenv
from google.adk import Agent


from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from logger_agent_base.agent import logger_agent_base
from callback_logger import CallbackLogger

# Load environment variables
load_dotenv()

async def process_user_input(runner, user_id, session_id, query, callback_logger):
    """Process a user query through the agent."""
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
                final_response_text = event.content.parts[0].text
                break
    
    # Print the final response if it was successfully generated
    if final_response_text:
        print("Final response:", final_response_text)
    
    # Fallback run_end logging if ADK callback doesn't fire (uses last state)
    if callback_logger:
        callback_logger.log_completion(None, final_response_text or 'No response', session_id, user_id, 'logger_agent')
    
    return final_response_text

async def main():
    # Create log file
    log_file = "agent_logs.jsonl"
    with open(log_file, "w") as f:
        f.write("")
    
    # Create a callback logger
    callback_logger = CallbackLogger(log_file)
    
    # Create agent with bound callbacks from the logger instance
    logger_agent = Agent(
        name=logger_agent_base.name,
        model=logger_agent_base.model,
        description=logger_agent_base.description,
        instruction=logger_agent_base.instruction,
        tools=logger_agent_base.tools,
        # Register callbacks as lists of bound methods
        before_agent_callback=[callback_logger.before_agent_callback],
        after_agent_callback=[callback_logger.after_agent_callback],
        before_model_callback=[callback_logger.before_model_callback],
        after_model_callback=[callback_logger.after_model_callback],
        before_tool_callback=[callback_logger.before_tool_callback],
        after_tool_callback=[callback_logger.after_tool_callback]
    )
    
    # Create a session service
    session_service = InMemorySessionService()
    
    # Create a session
    session_id = str(uuid.uuid4())
    session = await session_service.create_session(
        app_name="CallbackDemo",
        user_id="example_user",
        session_id=session_id
    )
    
    # Create a runner with the fully configured agent
    runner = Runner(
        agent=logger_agent,
        app_name="CallbackDemo",
        session_service=session_service
    )
    
    # Interactive chat loop
    print("\nADK Callback Demo")
    print("Type 'exit' or 'quit' to end the conversation")
    print("--------------------------------------------------------")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye! Check agent_logs.jsonl for the interaction logs.")
            break
        
        # Process the user input (pass callback_logger for fallback)
        await process_user_input(runner, "example_user", session_id, user_input, callback_logger)

if __name__ == "__main__":
    asyncio.run(main())