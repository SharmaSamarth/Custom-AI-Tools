import os
import requests

from dotenv import load_dotenv
from langchain_core.tools import tool

from database import query_database

load_dotenv()


# =========================================================
# TOOL 1: CALCULATOR
# =========================================================

@tool
def calculator(expression: str) -> str:
    """
    Perform basic mathematical calculations.

    Example:
    125 * 48
    (25 + 10) / 5
    1000 * 0.10
    """

    try:
        allowed_characters = set(
            "0123456789+-*/().% "
        )

        if not set(expression) <= allowed_characters:
            return "Invalid mathematical expression."

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return f"Calculation result: {result}"

    except Exception as e:
        return f"Calculation error: {e}"


# =========================================================
# TOOL 2: WEATHER API
# =========================================================

@tool
def weather_lookup(city: str) -> str:
    """
    Get the current weather for a city using the OpenWeather API.
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return (
            "OPENWEATHER_API_KEY is missing. "
            "Please add it to the .env file."
        )

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 404:
            return f"Weather information not found for {city}."

        response.raise_for_status()

        data = response.json()

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        description = data["weather"][0]["description"]

        wind_speed = data["wind"]["speed"]

        return (
            f"Weather for {city.title()}:\n"
            f"Temperature: {temperature}°C\n"
            f"Feels like: {feels_like}°C\n"
            f"Condition: {description}\n"
            f"Humidity: {humidity}%\n"
            f"Pressure: {pressure} hPa\n"
            f"Wind speed: {wind_speed} m/s"
        )

    except requests.exceptions.RequestException as e:
        return f"Weather API error: {e}"


# =========================================================
# TOOL 3: DATABASE QUERY
# =========================================================

@tool
def database_query(sql_query: str) -> str:
    """
    Query the company SQLite database.

    The database contains an employees table with:
    id, name, role, department, salary.

    Use SELECT queries only.
    """

    sql_query = sql_query.strip()

    # Safety check
    if not sql_query.lower().startswith("select"):
        return "Only SELECT queries are allowed."

    result = query_database(sql_query)

    if isinstance(result, str):
        return result

    if not result:
        return "No records found."

    return str(result)


# List of tools given to the agent
tools = [
    calculator,
    weather_lookup,
    database_query
]