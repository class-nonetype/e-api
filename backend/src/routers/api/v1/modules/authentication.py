from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR
)

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
        return Response(status_code=HTTP_400_BAD_REQUEST, content={'message': 'No se pudo crear el usuario. Por favor intentelo de nuevo.'})

    user = create_user(session=session, schema=schema)

    return Response(
        content={'message': 'El usuario ha sido creado.'},
        status_code=HTTP_201_CREATED,
    )




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
async def validate_session(Authorization: str, request: Request, session: Session = Depends(database)):
    logger.info(msg='{0}:{1}'.format(request.client.host, request.client.port))

    decoded_token = verify_access_token(token=Authorization, output=True)

    user_id = decoded_token['user_id']
    user_role_id = decoded_token['role_id']

    # Sesión del usuario
    user_session = {
        'client': request.client.host,
        'user_id': user_id,
        'access_token': Authorization
    }

    return user_session
