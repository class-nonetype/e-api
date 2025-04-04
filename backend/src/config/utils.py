import pytz

from os import getenv
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


DATABASE_URL = getenv('DATABASE_URL', None)
SECRET_KEY = getenv('SECRET_KEY', None)
TIMEZONE = pytz.timezone(zone=getenv('TIMEZONE'))





def get_datetime():
    return datetime.now(tz=TIMEZONE)

