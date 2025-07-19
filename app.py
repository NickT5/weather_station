from flask import Flask, render_template, request
import os
from weather_station import WeatherStation

app = Flask(__name__)
weather_station = WeatherStation()


@app.route("/", methods=["GET", "POST"])
def index():
    """Home page with weather search form"""
    weather_data = None
    location_name = None
    error = None

    if request.method == "POST":
        location = request.form.get("location", "").strip()

        if location:
            # Get coordinates
            lat, lon, location_name = weather_station.get_coordinates(location)

            if lat is None:
                error = f"Could not find location: {location}"
            else:
                # Get weather data
                weather_data = weather_station.get_weather_data(lat, lon)

                if weather_data is None:
                    error = "Failed to fetch weather data. Please try again."

    return render_template("index.html", weather_data=weather_data, location_name=location_name, error=error)


@app.route("/about")
def about():
    """About page with information about the application"""
    return render_template("about.html")


@app.template_filter("get_weather_description")
def get_weather_description_filter(weather_code):
    """Template filter to convert weather code to description"""
    return weather_station.get_weather_description(weather_code)


@app.template_filter("celsius_to_fahrenheit")
def celsius_to_fahrenheit_filter(celsius):
    """Template filter to convert Celsius to Fahrenheit"""
    return (celsius * 9 / 5) + 32


if __name__ == "__main__":
    # Create templates directory if it doesn't exist
    if not os.path.exists("templates"):
        os.makedirs("templates")

    # Get host and port from environment variables with defaults
    host = os.environ.get("WEATHER_HOST", "0.0.0.0")
    port = int(os.environ.get("WEATHER_PORT", 5000))
    debug = os.environ.get("WEATHER_DEBUG", "True").lower() == "true"

    # Run the Flask app
    app.run(host=host, port=port, debug=debug)
