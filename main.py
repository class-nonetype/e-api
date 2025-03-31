from src.config.utils import (
    API_TITLE,
    API_DESCRIPTION,
    API_VERSION,
    API_TIMEZONE,
    API_HOST,
    API_PORT
)
from src.routers.api.router import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run



app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION) #, lifespan=lifespan)
app.timezone = API_TIMEZONE
app.include_router(router=router)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
) 


if __name__ == '__main__':
    run(app=app, host=API_HOST, port=API_PORT)