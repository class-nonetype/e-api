from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from src.config.utils import get_datetime
from src.config.log import logger
from src.database.session import database
from src.database.queries.user import (
    select_user_account_by_username,
    update_last_login_date,
    validate_user_authentication,
    create_user
)

from src.models.schemas.user import UserAccount, CreateUserAccount
from src.config.tokens.jwt import (
    create_access_token, verify_access_token,
    JWTBearer
)

from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse



router = APIRouter()
authentication_schema = HTTPBearer()

@router.post(
    path='/sign-in',
    status_code=HTTP_200_OK,
    tags=['Autenticación'],
    description=(
        ''
    ),
    summary='',
)
async def sign_in(schema: UserAccount, request: Request, session: Session = Depends(database)):
    logger.info(msg='{0}:{1}'.format(request.client.host, request.client.port))
    
    try:
        user_authentication = validate_user_authentication(session=session, username=schema.username, password=schema.password)

        if not user_authentication:
            return Response(status_code=HTTP_401_UNAUTHORIZED)
        
        user_credential = {
            'user_account_id': user_authentication.id.hex,
            'username': user_authentication.username,
        }
        user_access_token = create_access_token(credential=user_credential)
        
        user_session = {
            'date': update_last_login_date(session=session, user_account_id=user_authentication.id),
            'client': request.client.host,
            'user_account_id': user_authentication.id.hex,
            'access_token': user_access_token
        }
        return user_session

    except Exception as exception:
        logger.exception(msg=exception)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)



@router.post(
    path='/sign-up',
    status_code=HTTP_201_CREATED,
    tags=['Autenticación'],
    description=(
        ''
    ),
    summary='',
)
async def sign_up(schema: CreateUserAccount, session: Session = Depends(database)):
    user = select_user_account_by_username(session=session, username=schema.UserAccount.username)
    if user:
        return Response(status_code=HTTP_400_BAD_REQUEST)
    del user

    user = create_user(session=session, schema=schema)

    return Response(status_code=HTTP_201_CREATED)




# Validador de sesión.
@router.post(
    path='/verify/session',
    tags=['Autenticación'],
    description=(
        ''
    ),
    summary='',
    dependencies=[Depends(JWTBearer())]
)
async def validate_session(Authorization: str, request: Request):
    logger.info(msg='{0}:{1}'.format(request.client.host, request.client.port))

    decoded_token = verify_access_token(token=Authorization, output=True)

    user_account_id = decoded_token['user_account_id']

    user_session = {
        'client': request.client.host,
        'user_account_id': user_account_id,
        'access_token': Authorization
    }

    return user_session
