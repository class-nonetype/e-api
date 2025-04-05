from pytz import timezone
from os import getenv
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()



DATABASE_URL = getenv('DATABASE_URL', None)
SECRET_KEY = getenv('SECRET_KEY', None)
TIMEZONE = timezone(zone=getenv('TIMEZONE', 'America/Santiago'))

API_TITLE = getenv('API_TITLE', None)
API_DESCRIPTION = getenv('API_DESCRIPTION', None)
API_VERSION = getenv('API_VERSION', None)
API_HOST = getenv('API_HOST', '0.0.0.0')
API_PORT = int(getenv('API_PORT', 8000))




def get_datetime():
    return datetime.now(tz=TIMEZONE)

