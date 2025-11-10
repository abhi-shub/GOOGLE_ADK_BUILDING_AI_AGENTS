from google.adk import Agent
from google.adk.tools import FunctionTool
import random

def get_weather(location: str, date: str) -> dict:
    """
    Get weather information for a specific location and date.

    Args:
        location: City or location name
        date: Date in YYYY-MM-DD format

    Returns:
        Weather information including temperature, conditions, and humidity
    """
    # In a real application, this would call a weather API
    # For this example, we'll generate random weather data
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Stormy", "Snowy"]
    temp_celsius = random.randint(5, 35)
    temp_fahrenheit = (temp_celsius * 9/5) + 32
    humidity = random.randint(30, 90)

    return {
        "location": location,
        "date": date,
        "temperature_celsius": temp_celsius,
        "temperature_fahrenheit": round(temp_fahrenheit, 1),
        "conditions": random.choice(conditions),
        "humidity": humidity,
        "data_source": "Simulated weather data (for demo purposes)"
    }

weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.5-flash-lite",
    description="Provides detailed weather information for specific locations and dates",
    instruction="""
    You are a helpful weather assistant that provides weather information.

    When asked about weather for a specific location and date, use the get_weather tool to fetch data.

    Present the weather information in a friendly, conversational manner. Include:
    - Temperature (in both Celsius and Fahrenheit)
    - Weather conditions
    - Humidity

    If the user doesn't specify a date, assume they're asking about the current date.
    If the user doesn't specify a location, ask them to provide one.
    """,
    tools=[FunctionTool(get_weather)]
)
