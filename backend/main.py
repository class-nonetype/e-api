from src.routers.api.router import router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from dotenv import load_dotenv
from os import getenv
from pytz import timezone
from pathlib import Path
from datetime import datetime



if not any([file.suffix == '.env' or file.name.endswith('.env')
            for file in Path(__file__).absolute().parent.parent.iterdir()]):
    exit()

else:
    load_dotenv()





def main(**kwargs) -> None:
    print(f'{datetime.now(tz=timezone(zone=kwargs['timezone']))=}')

    app = FastAPI(
        title=kwargs['api_title'],
        description=kwargs['api_description'],
        version=kwargs['api_version']
    )
    app.timezone = timezone(zone=kwargs['timezone'])
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
        host=kwargs['api_host'],
        port=int(kwargs['api_port'])
    )



if __name__ == '__main__':
    main(
        timezone=getenv('TIMEZONE'),
        api_title=getenv('API_TITLE'),
        api_description=getenv('API_DESCRIPTION'),
        api_version=getenv('API_VERSION'),
        api_host=getenv('API_HOST'),
        api_port=getenv('API_PORT'),
    )