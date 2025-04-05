from fastapi import APIRouter

from src.config.log import logger
from src.config.api import API_PREFIX
from src.routers.api.v1.modules import authentication, application

# Diccionario que contiene las rutas de la API categorizadas por tipo de módulo.
API_ROUTERS = {
    'application': [application.router],
    'authentication': [authentication.router]
}

# Crea una instancia del enrutador de FastAPI.
router = APIRouter()

# Incluye todas las rutas del diccionario API_ROUTERS en el enrutador global.
# Para cada tipo de módulo, las rutas se agregan con el prefijo correspondiente.
for key, values in API_ROUTERS.items():
    for value in values:
        logger.debug(msg=API_PREFIX[key])
        router.include_router(
            router=value,              # El router de cada módulo.
            prefix=API_PREFIX[key]     # El prefijo que se define según el tipo de módulo.
        )
