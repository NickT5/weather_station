import sys

from weather_station import WeatherStation


def main():
    """Entry point of the application"""
    if len(sys.argv) > 1:
        # Command line argument mode
        location = " ".join(sys.argv[1:])
        weather_station = WeatherStation()

        print(f"🔍 Getting weather for: {location}")
        lat, lon, location_name = weather_station.get_coordinates(location)

        if lat is None:
            print(f"❌ Could not find location: {location}")
            sys.exit(1)

        weather_data = weather_station.get_weather_data(lat, lon)
        if weather_data is None:
            print("❌ Failed to fetch weather data.")
            sys.exit(1)

        weather_station.format_weather_report(weather_data, location_name, lat, lon)
    else:
        # Interactive mode
        weather_station = WeatherStation()
        weather_station.run()


def system_info():
    print(sys.executable)
    print(sys.version)


if __name__ == "__main__":
    main()
