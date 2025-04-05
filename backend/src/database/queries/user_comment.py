import bcrypt

from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from uuid import (UUID, uuid4)
from typing import Literal

from src.config.utils import get_datetime, get_modification_date_status
from src.config.log import logger
from src.database.models.user_comments import UserComments
from src.models.schemas.user_comment import CreateUserComment, ModifyUserComment, DeleteUserComment

def create_user_comment(session: Session, schema: CreateUserComment) -> UserComments:
    user_comment = UserComments(
        id=uuid4(),
        user_id=schema.user_id,
        item_id=schema.item_id,
        institution_id=schema.institution_id,
        register_id=schema.register_id,
        reply_id=schema.reply_id,
        type_id=schema.type_id,
        text=schema.text,
        full_name=schema.full_name,
        active=True,
        public=schema.public,
        creation_date=get_datetime(),
        modification_date=get_datetime()
    )
    session.add(user_comment)
    session.commit()
    session.refresh(user_comment)
    
    return user_comment


def update_user_comment(session: Session, schema: ModifyUserComment, user_comment_id: UUID) -> (bool | None):
    user_comment = session.query(UserComments).filter(and_(UserComments.id==user_comment_id, UserComments.active == True)).first()
    
    if not user_comment:
        return None
    
    if get_modification_date_status(date=user_comment.creation_date):
        user_comment.text = str(schema.text)
        user_comment.modification_date = get_datetime()

        session.commit()
        session.refresh(user_comment)
        
        return True
    else:
        return False


def delete_user_comment(session: Session, user_comment_id: UUID) -> (Literal[True] | None):
    user_comment = session.query(UserComments).filter(and_(UserComments.id==user_comment_id)).first()

    if not user_comment:
        return None

    user_comment.active = False

    session.commit()
    session.refresh(user_comment)

    return True
