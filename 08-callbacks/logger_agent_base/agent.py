from google.adk import Agent
from google.adk.tools import FunctionTool
from datetime import datetime
from typing import List, Any

def get_current_time() -> dict:
    """
    Returns the current time.
    Use this when the user asks for the current time.
    """
    now = datetime.now()
    
    return {
        "current_time": now.strftime("%H:%M:%S"),
        "current_date": now.strftime("%Y-%m-%d"),
        "timezone": datetime.now().astimezone().tzname()
    }

# Base agent without callbacks (callbacks added in main.py)
logger_agent_base = Agent(
    name="logger_agent",
    model="gemini-2.5-flash",
    description="A helpful agent that demonstrates ADK lifecycle callbacks.",
    instruction="""
    You are a helpful assistant that can provide information and answer questions.
    
    When asked about the current time, use the get_current_time tool.
    
    Be friendly and conversational in your responses.
    """,
    tools=[FunctionTool(get_current_time)]
)