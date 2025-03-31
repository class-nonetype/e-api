import pytz

from os import getenv
from logging import Formatter
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


DATABASE_URL = getenv('DATABASE_URL', None)
SECRET_KEY = getenv('SECRET_KEY', None)
TIMEZONE = pytz.timezone(zone=getenv('TIMEZONE'))


PACKAGE_DIRECTORY_PATH = Path(__file__).resolve().parent.parent
STORAGE_DIRECTORY_PATH = (PACKAGE_DIRECTORY_PATH / 'storage')
TEMP_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'temp')
UPLOAD_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'uploads')
BACKUP_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'backups')
DATABASE_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'database')


LOG_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'logs')
LOG_FILE_NAME = 'events.log' 
LOG_FILE_PATH = (LOG_DIRECTORY_PATH / LOG_FILE_NAME)
LOG_FORMATTER = Formatter(
    fmt='%(asctime)-10s %(levelname)-10s %(filename)-10s -> %(funcName)s::%(lineno)s: %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p',
    style='%'
)



def create_directory(*args):
    for directory in args:
        if not directory.exists():
            directory.mkdir()

def get_datetime(): return datetime.now(tz=TIMEZONE)

create_directory(
    STORAGE_DIRECTORY_PATH,
    TEMP_DIRECTORY_PATH,
    UPLOAD_DIRECTORY_PATH,
    LOG_DIRECTORY_PATH,
    BACKUP_DIRECTORY_PATH,
    DATABASE_DIRECTORY_PATH
)
