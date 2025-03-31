import sqlalchemy.orm
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)

from src.config.log import logger
from src.database.session import database
from src.models.schemas.user import UserAccount
from src.config.security.jwt import (
    create_access_token, verify_access_token,
    JWTBearer
)

from fastapi import APIRouter, Request, Response, Depends
from fastapi.security import HTTPBearer


from src.functions.authentication import validate_user_authentication


router = APIRouter()
authentication_schema = HTTPBearer()

@router.post(
    path='/sign-in',
    tags=['Autenticación'],
    description=(
        ''
    ),
    summary='',
)
async def sign_in(schema: UserAccount, request: Request, session: sqlalchemy.orm.Session = Depends(database)):
    logger.info(msg='{0}:{1}'.format(request.client.host, request.client.port))
    
    try:
        user_authentication = validate_user_authentication(session=session, username=schema.username, password=schema.password)

        if not user_authentication:
            return Response(status_code=HTTP_401_UNAUTHORIZED)

        return Response(status_code=HTTP_200_OK)

    except Exception as exception:
        logger.exception(msg=exception)
        raise exception
