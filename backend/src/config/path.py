from pathlib import Path

def create_directory(*args):
    for directory in args:
        if not directory.exists():
            directory.mkdir()




PACKAGE_DIRECTORY_PATH = Path(__file__).resolve().parent.parent
STORAGE_DIRECTORY_PATH = (PACKAGE_DIRECTORY_PATH / 'storage')
TEMP_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'temp')
UPLOAD_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'uploads')
BACKUP_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'backups')
DATABASE_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'database')

LOG_DIRECTORY_PATH = (STORAGE_DIRECTORY_PATH / 'logs')
LOG_FILE_NAME = 'events.log' 
LOG_FILE_PATH = (LOG_DIRECTORY_PATH / LOG_FILE_NAME)


create_directory(
    STORAGE_DIRECTORY_PATH,
    TEMP_DIRECTORY_PATH,
    UPLOAD_DIRECTORY_PATH,
    LOG_DIRECTORY_PATH,
    BACKUP_DIRECTORY_PATH,
    DATABASE_DIRECTORY_PATH
)


print(
    f'{PACKAGE_DIRECTORY_PATH=}'
)