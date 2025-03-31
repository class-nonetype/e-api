import logging
import time
import uuid
from src.config.utils import (LOG_FILE_PATH, LOG_FORMATTER)
logging.Formatter.converter = time.gmtime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Borrar contenido del archivo actual
with open(file=LOG_FILE_PATH, mode='w') as log_file:
    pass


LOG_FILE_HANDLER = logging.FileHandler(filename=LOG_FILE_PATH, mode='+a', encoding='utf-8')
LOG_FILE_HANDLER.setFormatter(fmt=LOG_FORMATTER)

# Instanciación del archivo de registro.
logger.addHandler(LOG_FILE_HANDLER)



# Filtro para ocultar encabezados sensibles
class FilterSensitiveHeaders(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:

        # Verificar si el mensaje es una cadena y contiene el formato del log
        if isinstance(record.msg, str):

            # Verificar y ocultar el 'Authorization' en los argumentos si están presentes
            if record.args:
                new_arguments = []
                for argument in record.args:
                    # Ocultar el token de acceso en los registros de los eventos del servidor
                    if isinstance(argument, str) and 'Authorization' in argument:
                        argument = argument.split('Authorization')
                        argument = '%s: <hidden>' % argument[0]
                        argument = argument.replace(argument[0], argument[0])
                    
                    # Ocultar la UUID en los registros de los eventos del servidor
                    if isinstance(argument, str):
                        for section in argument.split('/'):
                            try:
                                section = uuid.UUID(section)
                                argument = argument.replace(str(section), '<hidden>')
                            except ValueError:
                                pass
                    new_arguments.append(argument)

                # Reemplazar los argumentos del registro con los valores filtrados
                record.args = tuple(new_arguments)

            # También se verifica el mensaje completo, en caso de que no sea parte de los args
            if 'Authorization' in record.msg:
                record.msg = record.msg.split('Authorization')
                record.msg = '%s: <hidden>' % record.msg[0]
                record.msg = record.msg.replace(record.msg[0], record.msg[0])
                print(f'{__file__} ::: {record.msg}')
        return True


# Modificar la configuración de Uvicorn con la finalidad de filtrar los registros con datos sensibles
# en este caso es la verificación de la sesión al recargar la vista
from uvicorn.config import LOGGING_CONFIG

LOGGING_CONFIG['filters'] = {
    'filter_sensitive_headers': {
        '()': FilterSensitiveHeaders,
    }
}

# Aplicar el filtro al logger de Uvicorn
LOGGING_CONFIG['loggers']['uvicorn.access']['filters'] = ['filter_sensitive_headers']

# Aplicar la configuración de logging
logging.config.dictConfig(LOGGING_CONFIG)

# Agregar el filtro al logger existente de Uvicorn
logging.getLogger('uvicorn.access').addFilter(FilterSensitiveHeaders())