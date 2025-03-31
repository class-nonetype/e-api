from sqlalchemy.orm.session import Session
from sqlalchemy import and_

from src.database.models.user_accounts import UserAccounts


def select_user_by_username(session: Session, username: str):
    return session.query(UserAccounts).filter(and_(UserAccounts.username==username, UserAccounts.active == True)).first()
