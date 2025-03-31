from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from uuid import UUID

from src.config.utils import get_datetime
from src.database.models.user_accounts import UserAccounts


def select_user_by_username(session: Session, username: str) -> (UserAccounts | None):
    return session.query(UserAccounts).filter(and_(UserAccounts.username==username, UserAccounts.active == True)).first()

def update_last_login_date(session: Session, user_account_id: UUID) -> None:
    session.query(UserAccounts).filter(and_(UserAccounts.id==user_account_id, UserAccounts.active == True)).update({'last_login_date': get_datetime()})
    return session.commit()
