from sqlalchemy.orm import Session
from starlette.status import (
    HTTP_200_OK, HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from src.config.log import logger
from src.database.session import database
from src.database.queries.user_comment import (
    create_user_comment,
    update_user_comment,
    delete_user_comment
)

from src.models.schemas.user_comment import CreateUserComment, ModifyUserComment
from src.config.tokens.jwt import (
    JWTBearer
)

from fastapi import APIRouter, Request, Response, Depends, HTTPException
from fastapi.security import HTTPBearer


from uuid import UUID


router = APIRouter()
authentication_schema = HTTPBearer()

@router.post(
    path='/comment',
    status_code=HTTP_201_CREATED,
    tags=['Comentario'],
    description=(
        ''
    ),
    summary='',
    dependencies=[Depends(JWTBearer())]
)
async def post_user_comment(schema: CreateUserComment, request: Request, session: Session = Depends(database)):
    logger.info(msg='{0}:{1}'.format(request.client.host, request.client.port))

    try:
        user_comment = create_user_comment(session=session, schema=schema)
        
        return Response(status_code=HTTP_400_BAD_REQUEST) if not user_comment else Response(status_code=HTTP_201_CREATED)

    except Exception as exception:
        logger.exception(msg=exception)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.put(
    path='/comment/{user_comment_id}',
    tags=['Comentario'],
    description=(
        ''
    ),
    summary='',
    dependencies=[Depends(JWTBearer())]
)
async def put_user_comment(Comment: ModifyUserComment, user_comment_id: UUID, request: Request, session: Session = Depends(database)):
    logger.info(msg='{0}:{1}'.format(request.client.host, request.client.port))

    try:
        user_comment = update_user_comment(session=session, schema=Comment, user_comment_id=user_comment_id)
        
        return Response(status_code=HTTP_404_NOT_FOUND) if not user_comment else Response(status_code=HTTP_200_OK)
        
    except Exception as exception:
        logger.exception(msg=exception)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete(
    path='/comment/{user_comment_id}',
    tags=['Comentario'],
    description=(
        ''
    ),
    summary='',
    dependencies=[Depends(JWTBearer())]
)
async def delete_user_comment(user_comment_id: UUID, request: Request, session: Session = Depends(database)):
    logger.info(msg='{0}:{1}'.format(request.client.host, request.client.port))

    try:
        user_comment = delete_user_comment(session=session, user_comment_id=user_comment_id)

        return Response(status_code=HTTP_404_NOT_FOUND) if not user_comment else Response(status_code=HTTP_200_OK)

    except Exception as exception:
        logger.exception(msg=exception)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR)


'''
@router.post(
    path='/attachment/institution/{institution_id}/item/{item_id}',
    tags=['Anexo'],
    dependencies=[fastapi.Depends(JWTBearer())]
)
async def post_annex(
    item_id: uuid.UUID,
    institution_id: uuid.UUID,
    register_id: uuid.UUID,
    request: fastapi.Request,
    document: fastapi.UploadFile = fastapi.File(...),
    session: sqlalchemy.orm.Session = fastapi.Depends(database)
):
    log.info(f'{request.client.host}:{request.client.port}')
    user_id = get_user_id_from_access_token(request=request)

    try:
        if not document.file:
            return fastapi.Response(
                status_code=starlette.status.HTTP_400_BAD_REQUEST,
                content='No se ha enviado un archivo válido.'
            )

        file_extension = os.path.splitext(document.filename)[1].lower()
        if file_extension not in ALLOWED_FILE_EXTENSIONS:
            return fastapi.Response(status_code=starlette.status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        
        file_uuid_name = str(uuid.uuid4()) + file_extension                 # Nombre del archivo con UUID
        file_key = AWS_S3_ANNEX_FILE_KEY + file_uuid_name                   # Llave del archivo en S3
        file_url = f'https://{AWS_BUCKET}.s3.amazonaws.com/{file_key}'      # URL del archivo en S3
        file_content = await document.read()                                # Lectura de contenido

        if not file_content:
            return fastapi.Response(
                status_code=starlette.status.HTTP_400_BAD_REQUEST,
                content='El archivo está vacío.'
            )

        file_content_type = document.content_type or 'application/octet-stream'

        log.debug(f'\n{file_uuid_name=}\n{file_key=}\n{file_content_type=}\n{len(file_content)=}\n')

        upload_file_to_aws_s3(
            aws_client=AWS_S3_CLIENT,
            aws_s3_bucket_name=AWS_BUCKET,
            file_key=file_key,
            file_content=file_content,
            file_content_type=file_content_type
        )

        annex = create_annex(
            session=session,
            user_id=user_id,
            item_id=item_id,
            institution_id=institution_id,
            register_id=register_id,
            file_path=file_key,
            file_url=file_url,
            file_size=len(file_content),
            file_name=document.filename,
            file_uuid_name=file_uuid_name
        )
        
        if not annex:
            return fastapi.Response(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)

        return fastapi.Response(status_code=starlette.status.HTTP_201_CREATED)

    except Exception as exception:
        log.exception(msg=exception)
        raise fastapi.Response(status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR)
'''