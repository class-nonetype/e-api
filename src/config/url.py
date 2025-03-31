API_VERSION = 'v1'
# Prefijos para las rutas de la API.
API_PREFIX = {
    'STATIC': '/api/{0}/static'.format(API_VERSION),                    # Prefijo para recursos estáticos.
    'APPLICATION': '/api/{0}/application'.format(API_VERSION),          # Prefijo para lógica de aplicación.
    'AUTHENTICATION': '/api/{0}/authentication'.format(API_VERSION)     # Prefijo para autenticación.
}