import fastapi
import fastapi.security

from src.config.url import API_PREFIX

# Importa los módulos que definen las rutas de la API de las diferentes funcionalidades.
from src.routers.api.v1.modules import authentication

# Diccionario que contiene las rutas de la API categorizadas por tipo de módulo.
API_ROUTERS = {
    #'APPLICATION': [  # Rutas relacionadas con la funcionalidad de la aplicación.
    #    user.router,
    #],
    'AUTHENTICATION': [  # Rutas relacionadas con la autenticación de usuarios.
        authentication.router
    ]
}

# Crea una instancia del enrutador de FastAPI.
router = fastapi.APIRouter()

# Incluye todas las rutas del diccionario API_ROUTERS en el enrutador global.
# Para cada tipo de módulo, las rutas se agregan con el prefijo correspondiente.
for key, values in API_ROUTERS.items():
    for value in values:
        router.include_router(
            router=value,              # El router de cada módulo.
            prefix=API_PREFIX[key]     # El prefijo que se define según el tipo de módulo.
        )
