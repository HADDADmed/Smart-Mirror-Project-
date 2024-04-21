import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def suggest_clothing(weather_data, user_preferences=None):
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"].lower()
    precipitation = weather_data.get("rain", {}).get("1h", 0)  # Rainfall in the last hour
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    humidity = weather_data["main"]["humidity"]
    snow = weather_data.get("snow", {}).get("1h", 0)  # Snowfall in the last hour

    # Define clothing categories and their associated weather conditions
    clothing_categories = {
        "warm weather": {"temp_min": 20, "temp_max": 40, "description": ["clear", "clouds"], "wind_speed_max": 10},
        "cold weather": {"temp_min": -10, "temp_max": 10, "humidity_max": 70},
        "rainy weather": {"precipitation": 1},
        "sunny weather": {"description": ["clear"], "humidity_max": 80},
        "snowy weather": {"snow": 1},
        "windy weather": {"wind_speed": 10},
        "hot weather": {"temp_min": 30, "temp_max": 50}
    }

    # Generate clothing recommendations based on current weather conditions
    recommendations = []
    for category, conditions in clothing_categories.items():
        if (conditions.get("temp_min", float("-inf")) <= temperature <= conditions.get("temp_max", float("inf"))) \
                or any(desc in description for desc in conditions.get("description", [])) \
                or (precipitation >= conditions.get("precipitation", 0)) \
                or (wind_speed >= conditions.get("wind_speed_min", 0) and wind_speed <= conditions.get("wind_speed_max", float("inf"))) \
                or (humidity <= conditions.get("humidity_max", float("inf"))) \
                or (snow >= conditions.get("snow", 0)):
            recommendations.append(category)

    # Personalize recommendations based on user preferences
    if user_preferences:
        personalized_recommendations = [category for category in recommendations if category in user_preferences.get("preferred_styles", [])]
        if personalized_recommendations:
            recommendations = personalized_recommendations

    return recommendations

def print_weather_data(weather_data, city):
    """Print weather data."""
    if weather_data:
        print(f"Weather in {city}")
        for key, value in weather_data["main"].items():
            print(f"{key.capitalize()}: {value}")
        for key, value in weather_data["wind"].items():
            print(f"{key.capitalize()}: {value}")
        for key, value in weather_data.get("rain", {"1h": 0}).items():
            print(f"Rainfall: {value} mm/hr")
        for key, value in weather_data.get("snow", {"1h": 0}).items():
            print(f"Snowfall: {value} mm/hr")
    else:
        print("Failed to fetch weather data for", city)

def main():
    # Simulated weather data
    weather_data = {
        "main": {"temp": 15, "humidity": 70},  # Temperature in Celsius, humidity in %
        "weather": [{"description": "Clear"}],
        "rain": {"1h": 0},  # Rainfall in mm/hr
        "wind": {"speed": 8},  # Wind speed in m/s
        "snow": {"1h": 0}  # Snowfall in mm/hr
    }

    # User preferences
    user_preferences = {
        "preferred_styles": ["warm weather", "sunny weather"]
    }

    # Get clothing recommendations based on weather data and user preferences
    clothing_recommendations = suggest_clothing(weather_data, user_preferences)
    
    # Print weather information
    print("Weather:")
    print_weather_data(weather_data, "Tangier")
    
    # Print clothing recommendations
    print("\nClothing Recommendations:")
    if clothing_recommendations:
        for recommendation in clothing_recommendations:
            print("-", recommendation)
    else:
        print("No clothing recommendations based on current weather.")

if __name__ == "__main__":
    main()
