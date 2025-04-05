import bcrypt

from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from uuid import (UUID, uuid4)
from typing import Literal

from src.config.utils import get_datetime
from src.config.log import logger
from src.database.models.user_accounts import UserAccounts
from src.database.models.user_profiles import UserProfiles
from src.models.schemas.user import CreateUserAccount



def select_user_by_username(session: Session, username: str) -> (UserAccounts | None):
    return session.query(UserAccounts).filter(and_(
        UserAccounts.username==username, UserAccounts.active == True
    )).first()


def validate_user_authentication(session: Session, username: str, password: str) -> (UserAccounts | Literal[False]):
    user = select_user_by_username(session=session, username=username)

    if not user:
        return False
    
    if not user.verify_password(password):
        return False

    if not user.active:
        return False

    return user


def update_last_login_date(session: Session, user_account_id: UUID) -> None:
    session.query(UserAccounts).filter(and_(
        UserAccounts.id==user_account_id, UserAccounts.active == True
    )).update({'last_login_date': get_datetime()})
    return session.commit()



def create_user_profile(**kwargs) -> UserProfiles:
    return UserProfiles(
        id=kwargs['id'],
        full_name=kwargs['full_name'],
        e_mail=kwargs['e_mail']
    )

def create_user_account(**kwargs) -> UserAccounts:
    return UserAccounts(
        id=kwargs['id'],
        role_id=kwargs['role_id'],
        profile_id=kwargs['profile_id'],
        username=kwargs['username'],
        password=kwargs['password']
    )

def create_user(session: Session, schema: CreateUserAccount) -> UserAccounts:
    try:
        user_profile = create_user_profile(
            id=uuid4(),
            full_name=schema.Profile.full_name,
            e_mail=schema.Profile.e_mail
        )
        session.add(user_profile)
        session.commit()

        user_account = create_user_account(
            id=uuid4(),
            role_id=schema.Role.id,
            profile_id=user_profile.id,
            username=schema.UserAccount.username,
            password=bcrypt.hashpw(
                password=schema.UserAccount.password.encode('utf-8'),
                salt=bcrypt.gensalt()
            ).decode('utf-8')
        )
        session.add(user_account)
        session.commit()
        
        return user_account

    except Exception as exception:
        session.rollback()

        logger.exception(msg=exception)
        raise exception
