# Weather Station

A simple weather application that provides current weather information for locations around the world. The application uses the Open-Meteo API.

## Features

- Command-line interface (CLI) for quick weather checks
- Web interface for a more visual experience
- Current weather conditions including temperature, humidity, pressure, and wind
- Support for location search by city and country name

## Usage

### Command Line Interface

Run the application in interactive mode:

```bash
uv run main.py
```

Or get weather for a specific location:

```bash
uv run main.py "London"
```

### Web Interface

Start the web server:

```bash
uv run app.py
```

Then open your browser and navigate to http://127.0.0.1:5000/

## Project Structure

- `main.py` - CLI entry point
- `app.py` - Web application entry point
- `weather_station.py` - Core functionality
- `templates/` - HTML templates for the web interface

## Technologies

- Python standard library (no external dependencies for core functionality)
- Flask (for web interface)
- Open-Meteo API (free weather data)
- uv (for dependency management and running the application)

## Development

uv provides several useful tools for development:

```bash
# View dependency tree
uv tree

# Install and run development tools
uv tool run ruff check --fix  # Run ruff to fix code style issues
uv tool run ruff format       # Format code with ruff
```
