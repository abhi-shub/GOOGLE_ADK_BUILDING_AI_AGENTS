from google.adk import Agent
from google.adk.tools import FunctionTool
import random

def get_weather(location: str) -> dict:
    """
    Get the current weather for a location.
    
    Args:
        location: City or location name
    
    Returns:
        Weather information including temperature, conditions, and humidity
    """
    # In a real application, this would call a weather API
    # For this example, we'll generate simulated weather data
    
    # Random temperature between 0 and 35°C
    temperature = round(random.uniform(0, 35), 1)
    
    # Random conditions
    conditions = random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy", "Snowy"])
    
    # Random humidity between 30% and 90%
    humidity = random.randint(30, 90)
    
    return {
        "location": location,
        "temperature_celsius": temperature,
        "temperature_fahrenheit": round((temperature * 9/5) + 32, 1),
        "conditions": conditions,
        "humidity": humidity,
        "forecast": "This is simulated weather data for demonstration purposes"
    }

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash",
    description="An agent that provides weather information",
    instruction="""
    You are a helpful weather assistant. When asked about the weather for a specific location,
    use the get_weather tool to fetch data.
    
    Present the weather information in a friendly, conversational manner. Include:
    - Temperature (in both Celsius and Fahrenheit)
    - Weather conditions
    - Humidity
    
    If the user doesn't specify a location, ask them to provide one.
    """,
    tools=[FunctionTool(get_weather)]
)

root_agent = weather_agent 
