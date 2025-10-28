from google.adk.agents.llm_agent import Agent

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.5-flash",
    description="A friendly agent that greets users",
    instruction="You are a helpful assistant that greets the user. Ask the user's name and greet them by their name."
)
