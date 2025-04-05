from typing import Union
from pytz import timezone
from os import getenv
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()





TIME_ALLOWED_MODIFICATION = getenv('TIME_ALLOWED_MODIFICATION', 72)

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


# Verifica si la fecha de modificación aún está dentro del tiempo habilitado.
def get_modification_date_status(date: Union[datetime, str]) -> bool:
    current_date = get_datetime()                       # Obtiene la fecha y hora actual con la zona horaria configurada.
    
    # Si hoy es miércoles (3) o jueves (4), se agregan 48 horas adicionales
    # al tiempo habilitado de modificación, siguiendo las políticas del sistema.
    if current_date.weekday() == 3 or current_date.weekday() == 4:
        current_date.replace(microsecond=0)
        time_allowed_modification = int(TIME_ALLOWED_MODIFICATION) + 48     # Redondeo de la hora actual para eliminar los microsegundos y asegurar precisión.
    else:
        current_date.replace(microsecond=0)
        time_allowed_modification = int(TIME_ALLOWED_MODIFICATION)          # En días distintos a miércoles o jueves, se usa el tiempo estándar configurado.
    
    # Asegura que la fecha de creación tenga una zona horaria asignada.
    # Si la fecha ya tiene tzinfo, esto puede lanzar un error.
    creation_date = TIMEZONE.localize(date)

    # Calcula la fecha límite de modificación sumando las horas permitidas.
    modification_deadline = creation_date + timedelta(hours=time_allowed_modification)
    
    # Si la fecha actual supera la fecha límite, la modificación no está permitida.
    return False if current_date > modification_deadline else True

