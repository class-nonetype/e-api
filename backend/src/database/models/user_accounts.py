from uuid import uuid4

from src.config.utils import get_datetime
from src.database.base import base as Base

import bcrypt

from src.database.models.user_roles import UserRoles
from src.database.models.user_profiles import UserProfiles

from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    DateTime,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



class UserAccounts(Base):

    __tablename__ = 'user_accounts'

    id                          = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_role_id                = Column(UUID(as_uuid=True), ForeignKey(UserRoles.id), nullable=False)
    user_profile_id             = Column(UUID(as_uuid=True), ForeignKey(UserProfiles.id), unique=True, nullable=False)
    username                    = Column(String, nullable=False)
    password                    = Column(String, nullable=False)
    creation_date               = Column(DateTime, default=lambda: get_datetime())
    last_login_date             = Column(DateTime, nullable=True)
    active                      = Column(Boolean, default=True, nullable=False)

    user_role_relation          = relationship('UserRoles', backref='user_account', uselist=False)
    user_profile_relation       = relationship('UserProfiles', backref='user_account', uselist=False)

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode('utf-8'),
            hashed_password=self.password.encode('utf-8')
        )

    def get_id(self) -> str:
        return str(self.id)

    def get_username(self) -> str:
        return self.username
