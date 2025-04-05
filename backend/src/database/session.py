import sqlalchemy.orm

from src.config.log import logger
from src.database.engine import engine

        
        
# Construye un generador de sesiones SQLAlchemy con configuraciones específicas.        
# La sesión es fundamental para interactuar con la base de datos de forma controlada.   
# - autocommit:        Desactiva la confirmación automática de transacciones,
#                      permitiendo mayor control sobre cuándo se confirma una operación.
#
# - autoflush:         Desactiva la actualización automática de los objetos en la
#                      sesión, evitando envíos innecesarios de datos a la base.
#
# - bind:              Asocia el motor (engine) creado previamente con las sesiones
#                      para establecer la conexión con la base de datos.
#
# - expire_on_commit:  Evita que los objetos expiren al confirmar la transacción,
#                      permitiendo un acceso más rápido a los datos ya cargados.
#
# Configuración específica de la sesión SQLAlchemy
SETTINGS = {
    'autocommit': False, 
    'autoflush': False, 
    'bind': engine, 
    'expire_on_commit': False
}

# Crea un generador de sesiones con la configuración definida.
session = sqlalchemy.orm.sessionmaker(**SETTINGS)


# Generador asíncrono de la sesión SQLAlchemy.
# Este generador proporciona una sesión de base de datos segura para cada petición.
async def database():
    database = session()
    try:
        yield database
    except Exception as exception:
        logger.exception(exception)
    finally:
        database.close()
