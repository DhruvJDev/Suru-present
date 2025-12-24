import requests
import os

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

# Load API key
load_dotenv()
API_KEY = os.getenv("openweather_api_key")

def wind_direction(degree):
    directions = ["North", "East",  "South",  "West"]
    index = round(degree / 45) % 8
    return directions[index]

def format_unix_time(timestamp, timezone_offset):
    utc_time = datetime.fromtimestamp(timestamp, timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime('%I:%M %p')

def get_weather(city_name):
    if not API_KEY:
        return "API key not found.", ""

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return f"Error: {data.get('message', 'City not found')}", ""

        city = data["name"]
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]


        # Spoken part
        spoken_report = (
            f"\nThe weather in {city} is currently {description}, "
            f"with a temperature of {temp}°C. "
            f"Humidity is {humidity}%. "
        )

        # Full report (includes spoken_report + technical details)
        point_report = (
            # f"Weather in {city}:\n\n"
            # f"{spoken_report}\n\n"
            f"\nTemperature: {temp}°C\n"
            f"Description: {description}\n"
            f"Humidity: {humidity}%\n"
        )

        return spoken_report, point_report

    except Exception as e:
        return f"Error: {str(e)}", ""
