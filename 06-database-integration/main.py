import os
import asyncio
import uuid
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService

from memory_agent.agent import memory_agent
from utils import call_agent_async

# Load environment variables
load_dotenv()

async def main():
    # Create a database session service
    # This will persist sessions to a SQLite database
    db_url = "sqlite:///./agent_sessions.db"
    session_service = DatabaseSessionService(db_url=db_url)
    
    # Define initial state for new sessions
    initial_state = {
        "username": "User",
        "reminders": []
    }
    
    # Application and user identifiers
    app_name = "ReminderApp"
    user_id = "abhi123"
    
    # Check if we have an existing session for this user
    existing_sessions = await session_service.list_sessions(
    app_name=app_name,
    user_id=user_id
    )
    
    session_list = existing_sessions.sessions # Extract the actual list
    if session_list: # Pythonic way to check if a list is non-empty
        # Use the existing session
        session_id = session_list[0].id
        print(f"Continuing existing session: {session_id}")
    else:
        # Create a new session
        session_id = str(uuid.uuid4())
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=initial_state
        )
        print(f"Created new session: {session_id}")
    
    # Create a runner with our agent and session service
    runner = Runner(
        agent=memory_agent,
        session_service=session_service,
        app_name=app_name
    )
    
    # Interactive chat loop
    print("\nReminder Agent Chat (Type 'exit' or 'quit' to end)")
    print("--------------------------------------------------------")
    
    while True:
        query = input("\nYou: ")
        
        if query.lower() in ["exit", "quit"]:
            print("Goodbye! Your reminders have been saved to the database.")
            break
        
        # Process the user input
        await call_agent_async(runner, app_name, user_id, session_id, query)

if __name__ == "__main__":
    asyncio.run(main())