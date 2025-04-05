from fastapi.security import (HTTPAuthorizationCredentials, HTTPBearer)
import datetime
import jwt

from fastapi import Request, HTTPException

from src.config.utils import (
    get_datetime, SECRET_KEY
)

from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN



def set_expiration_date(hours: int) -> str:
    expiration_date = get_datetime() + datetime.timedelta(hours=hours)
    return expiration_date.strftime('%Y-%m-%d %H:%M:%S.%f%z')


def create_access_token(credential: dict) -> str:
    return jwt.encode(
        payload={**credential, 'expires': set_expiration_date(hours=8)},
        key=SECRET_KEY,
        algorithm='HS256'
    )

def verify_access_token(token: str, output: bool = False):
    try:
        decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        expiration_date = datetime.datetime.strptime(decoded_token['expires'], '%Y-%m-%d %H:%M:%S.%f%z')
        current_date = get_datetime()

        if (output and expiration_date < current_date):
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Token expirado.')

        return decoded_token

    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Token inválido.')

def decode_access_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        expiration_date = datetime.datetime.strptime(decoded_token['expires'], '%Y-%m-%d %H:%M:%S.%f%z')
        current_date = datetime.datetime.now(expiration_date.tzinfo)

        if (expiration_date > current_date):
            return decoded_token

    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Token inválido.')



class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credential: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credential:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Código de autorización inválido.')

        if not credential.scheme == 'Bearer':
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Esquema de autorización inválida.')
        
        if not self.validate_jwt(credential.credentials):
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Token inválido o token expirado.')
        
        return credential.credentials

    def validate_jwt(self, token: str) -> bool:
        token_validity = False

        try:
            payload = decode_access_token(token)
        except:
            payload = None
        if payload:
            token_validity = True
        return token_validity

