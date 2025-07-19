# !/usr/bin/env python3
"""
Simple Weather Station CLI App
Uses Open-Meteo API (no API key required)
Built with Python standard library only
"""

import json
import urllib.request
import urllib.parse


class WeatherStation:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    def get_coordinates(self, location):
        """Get latitude and longitude for a given location"""
        try:
            # Encode the location for URL
            encoded_location = urllib.parse.quote(location)
            url = f"{self.geocoding_url}?name={encoded_location}&count=1&language=en&format=json"

            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())

            if not data.get("results"):
                return None, None, None

            result = data["results"][0]
            return result["latitude"], result["longitude"], result["name"]

        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None, None, None

    def get_weather_data(self, latitude, longitude):
        """Fetch weather data from Open-Meteo API"""
        try:
            # Parameters for current weather
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,surface_pressure,weather_code,wind_speed_10m,wind_direction_10m",
                "timezone": "auto",
            }

            # Build URL
            query_string = urllib.parse.urlencode(params)
            url = f"{self.base_url}?{query_string}"

            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())

            return data

        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_weather_description(self, weather_code):
        """Convert weather code to human-readable description"""
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }
        return weather_codes.get(weather_code, f"Unknown weather code: {weather_code}")

    def format_weather_report(self, weather_data, location_name, latitude, longitude):
        """Format and display weather information"""
        current = weather_data["current"]

        print("\n" + "=" * 50)
        print("🌤️  WEATHER STATION REPORT")
        print("=" * 50)

        # Location info
        print(f"📍 Location: {location_name}")
        print(f"   Coordinates: {latitude:.4f}°, {longitude:.4f}°")
        print(f"   Time: {current['time']}")

        print("\n" + "-" * 30)
        print("🌡️  CURRENT CONDITIONS")
        print("-" * 30)

        # Temperature
        temp_c = current["temperature_2m"]
        temp_f = (temp_c * 9 / 5) + 32
        print(f"Temperature: {temp_c}°C ({temp_f:.1f}°F)")

        # Weather condition
        weather_desc = self.get_weather_description(current["weather_code"])
        print(f"Conditions: {weather_desc}")

        # Humidity
        humidity = current["relative_humidity_2m"]
        print(f"Humidity: {humidity}%")

        # Pressure
        pressure = current["surface_pressure"]
        print(f"Pressure: {pressure} hPa")

        # Wind
        wind_speed = current["wind_speed_10m"]
        wind_direction = current["wind_direction_10m"]
        print(f"Wind: {wind_speed} km/h from {wind_direction}°")

        print("=" * 50)

    def run(self):
        """Main application loop"""
        print("🌤️  Welcome to Weather Station CLI!")
        print("Enter 'quit' or 'exit' to stop the program")

        while True:
            try:
                location = input("\n📍 Enter location (city, country): ").strip()

                if location.lower() in ["quit", "exit", "q"]:
                    print("Thanks for using Weather Station CLI! 👋")
                    break

                if not location:
                    print("Please enter a valid location.")
                    continue

                print(f"🔍 Searching for '{location}'...")

                # Get coordinates
                lat, lon, location_name = self.get_coordinates(location)
                if lat is None:
                    print(f"❌ Could not find location: {location}")
                    print("Try being more specific (e.g., 'London, UK' or 'New York, USA')")
                    continue

                print(f"📡 Fetching weather data for {location_name}...")

                # Get weather data
                weather_data = self.get_weather_data(lat, lon)
                if weather_data is None:
                    print("❌ Failed to fetch weather data. Please try again.")
                    continue

                # Display weather report
                self.format_weather_report(weather_data, location_name, lat, lon)

            except KeyboardInterrupt:
                print("\n\nExiting Weather Station CLI... 👋")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                print("Please try again.")
