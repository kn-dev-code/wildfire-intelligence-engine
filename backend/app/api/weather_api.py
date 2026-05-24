import os
from dotenv import load_dotenv

load_dotenv()
weather_api = os.getenv("WEATHER_API")
base_url = "https://api.openweathermap.org/data/2.5/weather"


