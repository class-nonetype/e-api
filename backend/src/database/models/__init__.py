# Registros
from src.config.log import logger

from src.database.base import base as Base
from src.database.engine import engine as Engine
from src.database.session import session as Session

from src.database.models.user_roles import UserRoles
from src.database.models.user_profiles import UserProfiles
from src.database.models.user_accounts import UserAccounts
from src.database.models.user_comments import UserComments
from src.database.models.user_file_uploads import UserFileUploads

from sqlalchemy import inspect
from sqlalchemy.orm import clear_mappers


# Bloque de creación de los modelos
try:
    Base.metadata.create_all(bind=Engine)
except Exception as exception:
    logger.exception(msg=exception)
    raise exception

'''
# Bloque de eliminación de los modelos
try:
    pass
	# database.Base.metadata.drop_all(bind=database.engine)
except Exception as exception:
    logger.exception(msg=exception)
    raise exception

# Bloque de verificación de los modelos
try:
    # Modelos
    models = {}

    # Sesión SQLAlchemy
    session = Session()

    # Objeto de inspección
    inspector = inspect(Engine)
    
    # El iterador 'model' tendrá como valor cada clase del modelo
    for model in [
        UserRoles,
        UserProfiles,
        UserAccounts
    ]:
        if inspector.has_table(model.__table__.name):
            # El diccionario 'models' insertará el estado del modelo iterado, con la finalidad
            # de verificar si el modelo existe como tabla en la base de datos.
            # Tendrá como valor True o False.
            models[model.__name__] = True

        else:
            models[model.__name__] = False
        

        if models[model.__name__]:
            logger.info(msg='%s\t<%s>' % (models[model.__name__], model.__name__))
        else:
            logger.error(msg='%s\t<%s>' % (models[model.__name__], model.__name__))
    del inspector
    del models

except Exception as exception:
    logger.exception(msg=exception)
'''
