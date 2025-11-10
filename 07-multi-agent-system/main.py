import os
import asyncio
import uuid
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
# from google.generativeai.types import content_types
# from google.generativeai.types.content_types import Part

# Import our agents
from vacation_planner.agent import vacation_planner
from weather_agent.agent import weather_agent
from travel_agent.agent import travel_agent

# Import utilities
from utils import process_user_input

# Load environment variables
load_dotenv()

async def main():
    # Create a session service
    session_service = InMemorySessionService()
    APP_NAME="VacationPlanner"

    # Create a session
    session_id = str(uuid.uuid4())
    user_id = "example_user"
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    
    # Create a runner with all our agents
    runner = Runner(
        agent=vacation_planner,
        app_name= APP_NAME,
        session_service=session_service
    )
    # Need to figure out the parameters of runner in case of multi agent system

    # Interactive chat loop
    print("\nVacation Planner Multi-Agent Demo")
    print("Type 'exit' or 'quit' to end the conversation")
    print("--------------------------------------------------------")
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Thank you for using the Vacation Planner! Goodbye!")
            break
        
        # Process the user input
        await process_user_input(runner, user_id, session_id, user_input)

if __name__ == "__main__":
    asyncio.run(main())

