import os
from dotenv import load_dotenv


load_dotenv()
nasa_api = os.getenv("NASA_MAP_KEY")
base_url = 'https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=' + nasa_api