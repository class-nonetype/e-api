from sqlalchemy.orm.session import Session

from src.database.queries.user import (UserAccounts, select_user_by_username)
from typing import Literal
from uuid import UUID


def validate_user_authentication(session: Session, username: str, password: str) -> (UserAccounts | Literal[False]):
    user = select_user_by_username(session=session, username=username)

    if not user:
        return False
    
    if not user.verify_password(password):
        return False

    if not user.active:
        return False

    return user

