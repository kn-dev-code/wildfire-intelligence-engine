import os
from dotenv import load_dotenv

load_dotenv()
weather_api = os.getenv("WEATHER_API")

def construct_weather_api(url: str):
  base_url = "https://api.openweathermap.org/data/2.5/weather"


