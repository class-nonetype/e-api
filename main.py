from src.routers.api.router import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from dotenv import load_dotenv
from os import getenv
from pytz import timezone
from pathlib import Path

if not any([file.name == '.env' for file in Path(__file__).absolute().parent.iterdir()]):
    ...


load_dotenv()

def main():
    app = FastAPI(
        title=getenv('API_TITLE'),
        description=getenv('API_DESCRIPTION'),
        version=getenv('API_VERSION')
        #lifespan=lifespan
    )
    app.timezone = timezone(zone=getenv('TIMEZONE'))
    app.include_router(router=router)
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    return run(
        app=app,
        host=getenv('API_HOST'),
        port=int(getenv('API_PORT'))
    )



if __name__ == '__main__':
    main()