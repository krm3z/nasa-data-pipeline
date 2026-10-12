from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

START_YEAR = 1995
END_YEAR   = datetime.now().year

APOD_URL = "https://api.nasa.gov/planetary/apod"

DB_PATH = "data/nasa.db"