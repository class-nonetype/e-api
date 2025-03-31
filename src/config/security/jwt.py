import fastapi.security
import datetime
import jwt

from src.config.utils import (
    TIMEZONE, get_datetime, SECRET_KEY
)




def set_expiration_date(hours: int) -> str:
    expiration_date = datetime.datetime.now(tz=TIMEZONE) + datetime.timedelta(hours=hours)
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
            return fastapi.responses.JSONResponse(content={'message': 'Token expirado'}, status_code=401)

        return decoded_token
    except jwt.exceptions.DecodeError:
        return fastapi.responses.JSONResponse(content={'message': 'Token inválido'}, status_code=401)

def decode_access_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        expiration_date = datetime.datetime.strptime(decoded_token["expires"], "%Y-%m-%d %H:%M:%S.%f%z")
        current_date = datetime.datetime.now(expiration_date.tzinfo)

        if (expiration_date > current_date):
            return decoded_token

    except jwt.exceptions.DecodeError:
        return fastapi.responses.JSONResponse(content={'message': 'Token inválido'}, status_code=401)



class JWTBearer(fastapi.security.HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: fastapi.Request):
        credential: fastapi.security.HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credential:
            if not credential.scheme == "Bearer":
                raise fastapi.HTTPException(status_code=403, detail="Esquema de autorización inválida.")
            
            if not self.validate_jwt(credential.credentials):
                raise fastapi.HTTPException(status_code=403, detail="Token inválido o token expirado.")
            
            return credential.credentials
        else:
            raise fastapi.HTTPException(status_code=403, detail="Código de autorización inválido.")

    def validate_jwt(self, token: str) -> bool:
        token_validity = False

        try:
            payload = decode_access_token(token)
        except:
            payload = None
        if payload:
            token_validity = True
        return token_validity

