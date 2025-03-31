import sqlalchemy.orm
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)

from src.config.log import logger
from src.database.session import database
from src.database.queries.user import update_last_login_date
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
        
        user_credential = {
            'user_id': user_authentication.id,
            'username': user_authentication.username,
            'role_id': user_authentication.role_id
        }
        user_access_token = create_access_token(credential=user_credential)
        update_last_login_date(session=session, account_id=user_authentication.id)

        user_session = {
            'client': request.client.host,
            'user_id': user_authentication.id,
            'access_token': user_access_token
        }
        return user_session

    except Exception as exception:
        logger.exception(msg=exception)
        raise exception
