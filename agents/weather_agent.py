import requests

class WeatherAgent:
    @staticmethod
    def get_weather(latitude, longitude):
        """Get the current weather at a location."""
        try:
            response = requests.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            )
            weather_data = response.json()
            return weather_data
        except Exception as error:
            return {"type": "error", "content": f"An error occurred: {error}"}
