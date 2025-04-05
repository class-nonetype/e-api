from src.config.utils import (
    TIMEZONE,
    API_TITLE,
    API_DESCRIPTION,
    API_HOST,
    API_PORT,
    API_VERSION
)
from src.routers.api.router import router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run


import platform

'''
from dotenv import load_dotenv
from pathlib import Path

if not any(
    [
        file.suffix == '.env'
        or file.name.endswith('.env')
        for file in Path(__file__).absolute().parent.parent.iterdir()
    ]):
    exit()

load_dotenv()
'''




def main(**kwargs) -> None:
    def create_app(**kwargs):
        app = FastAPI(
            title=kwargs['api_title'],
            description=kwargs['api_description'],
            version=kwargs['api_version']
        )
        app.timezone = kwargs['timezone']
        app.include_router(router=router)
        app.add_middleware(
            middleware_class=CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
        return app
    
    app = create_app(**kwargs)

    return run(
        app=app,
        host=kwargs['api_host'],
        port=kwargs['api_port'],
        use_colors=True if platform.system() == 'Windows'and platform.release() == '11' else False
    )


if __name__ == '__main__':
    main(
        timezone=TIMEZONE,
        api_title=API_TITLE,
        api_description=API_DESCRIPTION,
        api_version=API_VERSION,
        api_host=API_HOST,
        api_port=API_PORT
    )