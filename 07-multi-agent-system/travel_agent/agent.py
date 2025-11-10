from google.adk import Agent
from google.adk.tools import FunctionTool
import random

def get_transportation_options(origin: str, destination: str, date: str) -> dict:
    """
    Get available transportation options between two locations.

    Args:
        origin: Starting location
        destination: End location
        date: Travel date in YYYY-MM-DD format

    Returns:
        Available transportation options with prices and durations
    """
    # In a real application, this would call a travel API
    # For this example, we'll generate simulated options

    # Calculate mock distance (just for demonstration)
    distance = random.randint(100, 2000)

    # Generate flight options
    flight_price = distance * (0.10 + (random.random() * 0.15))
    flight_duration = distance / 800 * 60  # minutes

    # Generate train options if distance is reasonable
    train_available = distance < 1000
    train_price = None
    train_duration = None
    if train_available:
        train_price = distance * (0.07 + (random.random() * 0.07))
        train_duration = distance / 120 * 60  # minutes

    # Generate car rental option
    car_price = 50 + (distance * 0.05)
    car_duration = distance / 80 * 60  # minutes

    return {
        "origin": origin,
        "destination": destination,
        "date": date,
        "distance_km": distance,
        "options": {
            "flight": {
                "available": True,
                "price_usd": round(flight_price, 2),
                "duration_minutes": round(flight_duration),
                "notes": "Direct flight"
            },
            "train": {
                "available": train_available,
                "price_usd": round(train_price, 2) if train_available else None,
                "duration_minutes": round(train_duration) if train_available else None,
                "notes": "Scenic route" if train_available else "No train service available"
            },
            "car_rental": {
                "available": True,
                "price_usd_per_day": round(car_price, 2),
                "estimated_travel_minutes": round(car_duration),
                "notes": "Fuel costs not included"
            }
        },
        "data_source": "Simulated travel data (for demo purposes)"
    }

def get_accommodation_options(location: str, check_in: str, check_out: str) -> dict:
    """
    Get available accommodation options for a specific location and dates.

    Args:
        location: City or destination
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format

    Returns:
        Available accommodation options with prices and amenities
    """
    # In a real application, this would call a hotel/accommodation API
    # For this example, we'll generate simulated options

    # Mock accommodation types
    hotel_types = [
        {"name": "Luxury Hotel", "price_factor": 2.5, "amenities": ["Pool", "Spa", "Restaurant", "Gym", "Room Service"]},
        {"name": "Boutique Hotel", "price_factor": 1.8, "amenities": ["Unique Design", "Restaurant", "Concierge"]},
        {"name": "Budget Hotel", "price_factor": 1.0, "amenities": ["Free WiFi", "Basic Breakfast"]},
        {"name": "Hostel", "price_factor": 0.4, "amenities": ["Shared Kitchen", "Common Area", "Lockers"]},
        {"name": "Apartment Rental", "price_factor": 1.5, "amenities": ["Kitchen", "Washer/Dryer", "Living Area"]}
    ]

    # Generate 3 random accommodation options
    base_price = 50 + (random.random() * 50)
    accommodations = []

    selected_types = random.sample(hotel_types, 3)
    for hotel_type in selected_types:
        price = base_price * hotel_type["price_factor"]
        accommodations.append({
            "name": f"{hotel_type['name']} in {location}",
            "type": hotel_type["name"],
            "price_per_night_usd": round(price, 2),
            "amenities": hotel_type["amenities"],
            "rating": round(3 + (random.random() * 2), 1),  # 3-5 star rating
            "location": f"{location} city center",
            "availability": "Available"
        })

    return {
        "location": location,
        "check_in": check_in,
        "check_out": check_out,
        "options": accommodations,
        "data_source": "Simulated accommodation data (for demo purposes)"
    }

travel_agent = Agent(
    name="travel_agent",
    model="gemini-2.5-flash-lite",
    description="Provides travel recommendations including transportation and accommodation options",
    instruction="""
    You are a helpful travel assistant that provides transportation and accommodation recommendations.

    When asked about travel options, use:
    - get_transportation_options tool for flights, trains, and car rentals
    - get_accommodation_options tool for hotels and other lodging

    Present options in a helpful, organized way, highlighting:
    - Best value options
    - Fastest/most convenient options
    - Any special features or considerations

    If the user doesn't provide specific dates or locations, ask for clarification.
    """,
    tools=[
        FunctionTool(get_transportation_options),
        FunctionTool(get_accommodation_options)
    ]
)
