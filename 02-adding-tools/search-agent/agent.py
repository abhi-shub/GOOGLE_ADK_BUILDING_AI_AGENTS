# agent.py

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

# 1. Define the agent instance using the specific name 'search_agent'
search_agent = Agent(
    name="search_agent",
    model="gemini-2.5-flash",
    description="An agent that can search the web for information",
    instruction="""
    You are a helpful assistant that can search the web for current information.
    Use the search tool to find answers to questions about recent events, facts,
    or any information the user requests.
    
    Be concise but thorough in your responses, providing relevant information from
    your search results.
    
    Always cite your sources when providing information from search results.
    """,
    tools=[google_search]
)

# 2. Assign the same object to 'root_agent' for the ADK framework to find.
# This ensures that if the ADK defaults to looking for 'root_agent', it finds it.
root_agent = search_agent 

# 3. Optionally, you can add more configurations or methods to the agent here if needed.

# Note: Ensure that the 'google_search' tool is correctly implemented and imported
# from the tools module for this agent to function properly.
