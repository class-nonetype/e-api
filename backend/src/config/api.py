API_VERSION = 'v1'
# Prefijos para las rutas de la API.
API_PREFIX = {
    'static': '/api/{0}/static'.format(API_VERSION),                    # Prefijo para recursos estáticos.
    'application': '/api/{0}/application'.format(API_VERSION),          # Prefijo para lógica de aplicación.
    'authentication': '/api/{0}/authentication'.format(API_VERSION)     # Prefijo para autenticación.
}
