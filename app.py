import requests
import time
import json
import os
from colorama import init, Fore, Style
import matplotlib.pyplot as plt
from tabulate import tabulate

init(autoreset=True)

API_KEY = "b985897be8faaca71b497de7f002b6a2"

CACHE_FILE = "weather_cache.json"
CACHE_DURATION = 600  # seconds (10 minutes)

def load_cache():
    """Load cached data from the cache file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    """Save the cache dictionary to the cache file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def get_weather(location, unit):
    """
    Retrieve the current weather for a given location.
    Checks the cache first and, if stale, makes a new API request.
    """
    cache = load_cache()
    current_time = time.time()
    cache_key = f"{location}_weather_{unit}"

    if cache_key in cache and (current_time - cache[cache_key]["timestamp"] < CACHE_DURATION):
        print("Using cached current weather data.\n")
        return cache[cache_key]["data"]

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"appid": API_KEY}

    # Determine if the location is a ZIP code (assuming US ZIP if 5 digits) or a city name
    if location.replace(" ", "").isdigit() and len(location.replace(" ", "")) == 5:
        params["zip"] = f"{location},us"
    else:
        params["q"] = location

    # Set the unit parameter (API accepts "metric" or "imperial")
    if unit == "c":
        params["units"] = "metric"
    elif unit == "f":
        params["units"] = "imperial"

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            cache[cache_key] = {"timestamp": current_time, "data": weather_data}
            save_cache(cache)
            return weather_data
        elif response.status_code == 404:
            print(f"{Fore.RED}Error: The city or ZIP code '{location}' was not found. Please check your input and try again.{Style.RESET_ALL}")
            return None
        else:
            print(f"Error fetching weather data: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        return None

def get_forecast(location, unit):
    """
    Retrieve the forecast (5-day/3-hour intervals) for the given location.
    Uses similar caching logic as get_weather.
    """
    cache = load_cache()
    current_time = time.time()
    cache_key = f"{location}_forecast_{unit}"

    if cache_key in cache and (current_time - cache[cache_key]["timestamp"] < CACHE_DURATION):
        print("Using cached forecast data.\n")
        return cache[cache_key]["data"]

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"appid": API_KEY}

    if location.replace(" ", "").isdigit() and len(location.replace(" ", "")) == 5:
        params["zip"] = f"{location},us"
    else:
        params["q"] = location

    if unit == "c":
        params["units"] = "metric"
    elif unit == "f":
        params["units"] = "imperial"

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            forecast_data = response.json()
            cache[cache_key] = {"timestamp": current_time, "data": forecast_data}
            save_cache(cache)
            return forecast_data
        elif response.status_code == 404:
            print(f"{Fore.RED}Error: The city or ZIP code '{location}' was not found. Please check your input and try again.{Style.RESET_ALL}")
            return None
        else:
            print(f"Error fetching forecast data: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching forecast data: {e}")
        return None

def get_weather_icon(description):
    """Return a simple ASCII icon based on the weather description."""
    desc = description.lower()
    if "clear" in desc:
        return "☀"
    elif "cloud" in desc:
        return "☁"
    elif "rain" in desc:
        return "☔"
    elif "snow" in desc:
        return "❄"
    elif "storm" in desc or "thunder" in desc:
        return "⚡"
    elif "mist" in desc or "fog" in desc:
        return "🌫"
    else:
        return ""

def display_weather(weather, unit):
    """Display current weather information in a formatted table."""
    try:
        city = weather.get("name", "Unknown Location")
        temp = weather["main"]["temp"]
        description = weather["weather"][0]["description"].capitalize()
        humidity = weather["main"]["humidity"]
        wind_speed = weather["wind"]["speed"]
        icon = get_weather_icon(description)
        temp_unit = "°C" if unit == "c" else "°F" if unit == "f" else "K"
        wind_unit = "m/s" if unit in ["c", ""] else "mph"

        # Table data
        table_data = [
            ["City", city],
            ["Temperature", f"{temp} {temp_unit} {icon}"],
            ["Weather", description],
            ["Humidity", f"{humidity}%"],
            ["Wind Speed", f"{wind_speed} {wind_unit}"],
        ]

        # Display Table
        print(f"\n{Fore.GREEN}Current Weather:{Style.RESET_ALL}")
        print(tabulate(table_data, tablefmt="fancy_grid"))
    except KeyError as e:
        print("Error parsing weather data:", e)


def display_forecast(forecast, unit):
    """
    Display a 5-day forecast by extracting data for approximately noon each day.
    Also, plot the temperature trend using Matplotlib.
    """
    try:
        forecasts_by_date = {}
        dates = []
        temperatures = []
        
        for entry in forecast.get("list", []):
            dt_txt = entry.get("dt_txt", "")
            if "12:00:00" in dt_txt:  # Select noon time data for each day
                date = dt_txt.split(" ")[0]  # Extract the date (YYYY-MM-DD)
                forecasts_by_date[date] = entry
                dates.append(date)
                temperatures.append(entry["main"]["temp"])

        if forecasts_by_date:
            temp_unit = "°C" if unit == "c" else "°F" if unit == "f" else "K"
            wind_unit = "m/s" if unit in ["c", ""] else "mph"
            
            print(f"\n{Fore.BLUE}5-Day Forecast (at approximately noon):{Style.RESET_ALL}")
            for date, data in forecasts_by_date.items():
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"].capitalize()
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                icon = get_weather_icon(description)
                print(f"{Fore.CYAN}{date}:{Style.RESET_ALL} {description} {icon}, Temp: {temp}{temp_unit}, Humidity: {humidity}%, Wind: {wind_speed} {wind_unit}")

            # 📊 **PLOT THE FORECAST GRAPH**
            plt.figure(figsize=(8, 5))
            plt.plot(dates, temperatures, marker='o', linestyle='-', color='b', label="Temperature")
            plt.xlabel("Date")
            plt.ylabel(f"Temperature ({temp_unit})")
            plt.title(f"5-Day Temperature Forecast")
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.legend()
            plt.xticks(rotation=45)
            plt.show()

        else:
            print("Forecast data is not available.")
    except Exception as e:
        print("Error displaying forecast data:", e)


def display_hourly_forecast(forecast, unit):
    """
    Display an hourly forecast (next 12 hours) and plot a line graph.
    """
    try:
        temp_unit = "°C" if unit == "c" else "°F" if unit == "f" else "K"
        wind_unit = "m/s" if unit in ["c", ""] else "mph"

        # Extract data for the next 12 hours
        hours = []
        temperatures = []
        
        print(f"\n{Fore.MAGENTA}Hourly Forecast (next 12 hours):{Style.RESET_ALL}")
        count = 0
        for entry in forecast.get("list", []):
            if count >= 4:  # 3-hour intervals, so 4 entries = 12 hours
                break
            dt_txt = entry.get("dt_txt", "")
            temp = entry["main"]["temp"]
            description = entry["weather"][0]["description"].capitalize()
            humidity = entry["main"]["humidity"]
            wind_speed = entry["wind"]["speed"]
            icon = get_weather_icon(description)

            # Store data for graph
            hours.append(dt_txt.split(" ")[1])  # Extract time (HH:MM:SS)
            temperatures.append(temp)

            # Print forecast details
            print(f"{Fore.CYAN}{dt_txt}:{Style.RESET_ALL} {description} {icon}, Temp: {temp}{temp_unit}, Humidity: {humidity}%, Wind: {wind_speed} {wind_unit}")

            count += 1

        # 📊 **PLOT THE HOURLY FORECAST GRAPH**
        plt.figure(figsize=(8, 5))
        plt.plot(hours, temperatures, marker='o', linestyle='-', color='g', label="Temperature")
        plt.xlabel("Time")
        plt.ylabel(f"Temperature ({temp_unit})")
        plt.title("Next 12 Hours Temperature Forecast")
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()

    except Exception as e:
        print("Error displaying hourly forecast data:", e)

def main():
    print(f"{Fore.GREEN}Simple Weather Forecast Application{Style.RESET_ALL}\n")
    while True:
        location = input("Enter the city name or ZIP code: ").strip()
        if not location:
            print("Error: Location cannot be empty.")
            return

        unit = input("Choose temperature unit - Enter C for Celsius or F for Fahrenheit (or press Enter for Kelvin): ").strip().lower()
        if unit not in ["c", "f"]:
            unit = ""  # Defaults to Kelvin if no valid unit is entered

        # Retrieve and display current weather data
        weather = get_weather(location, unit)
        if weather:
            display_weather(weather, unit)
        else:
            print("Could not retrieve weather data.")
            return

        # Ask the user for forecast preference: 5-day or hourly
        forecast_option = input("\nWould you like to see a forecast? Enter '5' for 5-day forecast, 'h' for hourly forecast, or 'n' for no forecast: ").strip().lower()
        if forecast_option in ["5", "h"]:
            forecast = get_forecast(location, unit)
            if forecast:
                if forecast_option == "5":
                    display_forecast(forecast, unit)
                elif forecast_option == "h":
                    display_hourly_forecast(forecast, unit)
            else:
                print("Could not retrieve forecast data.")
        else:
            print("No forecast selected.")
        while True:
            flag = input("Would you like to check the weather for another city? Press 'y' for yes or 'n' to exit: ").lower()
            if flag == 'y':
                break  
            elif flag == 'n':
                print(f"{Fore.GREEN}Thank you for using the weather app!{Style.RESET_ALL}")
                return
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'. Try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()