import os
from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv # New Import

# --- Load the environment variables before accessing them ---
load_dotenv()

# Get the OpenRouter API key from environment variables
openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")

# print("OpenRouter API Key:", openrouter_api_key)

# Set up the model using LiteLLM with OpenRouter and Anthropic's Claude
model = LiteLlm(
    model="openrouter/anthropic/claude-3-opus-20240229",
    api_key= openrouter_api_key
)

claude_agent = Agent(
    name="claude_agent",
    model=model,
    description="An agent powered by Anthropic's Claude that tells stories",
    instruction="""
    You are a creative storytelling assistant powered by Anthropic's Claude model.
    
    When asked to tell a story:
    1. Ask for a topic or theme if not provided
    2. Create an engaging, original short story on the topic
    3. Use vivid descriptions and interesting characters
    
    For other queries, respond normally using your knowledge and abilities.
    
    Be imaginative, eloquent, and conversational in your responses.
    """
)

root_agent = claude_agent


# Note: Ensure that the OPENROUTER_API_KEY environment variable is set correctly