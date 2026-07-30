from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

START_YEAR = 1995
END_YEAR   = datetime.now().year
DONKI_START_YEAR = 2010


APOD_URL = "https://api.nasa.gov/planetary/apod"
NEOWS_URL = "https://api.nasa.gov/neo/rest/v1/feed"
DONKI_URL = "https://api.nasa.gov/DONKI/CMEAnalysis"

DB_PATH = "data/nasa.db"