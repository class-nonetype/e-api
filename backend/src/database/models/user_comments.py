import uuid
from src.config.utils import get_datetime
from src.database.base import base as Base

from src.database.models.user_accounts import UserAccounts

from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    DateTime,
    Text,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship



class UserComments(Base):

    __tablename__           = 'user_comments'

    id                      = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_account_id         = Column(UUID(as_uuid=True), ForeignKey(UserAccounts.id), nullable=False)
    full_name               = Column(String, nullable=True)
    text                    = Column(Text, nullable=True)
    active                  = Column(Boolean, default=True, nullable=False)
    public                  = Column(Boolean, default=True, nullable=False)
    creation_date           = Column(DateTime, default=lambda: get_datetime())
    modification_date       = Column(DateTime, nullable=True, default=lambda: get_datetime())

    user_account_relation   = relationship('UserAccounts', backref='user_comment', uselist=False, foreign_keys=[user_account_id])

