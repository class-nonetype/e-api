from uuid import uuid4
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

from src.config.utils import get_datetime
from src.database.base import base as Base

from src.database.models.user_accounts import UserAccounts


class UserFileUploads(Base):
    __tablename__           = 'user_file_uploads'

    id                      = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    user_account_id         = Column(UUID(as_uuid=True), ForeignKey(UserAccounts.id), nullable=False)
    file_path               = Column(Text, nullable=True)
    file_url                = Column(Text, nullable=True)
    file_size               = Column(String, nullable=True)
    file_name               = Column(String, nullable=True)
    file_uuid_name          = Column(String, nullable=True)
    active                  = Column(Boolean, default=True, nullable=False)
    creation_date           = Column(DateTime, default=lambda: get_datetime())
    modification_date       = Column(DateTime, nullable=True, default=lambda: get_datetime())

    user_account_relation   = relationship('UserAccounts', backref='user_file_upload', uselist=False, foreign_keys=[user_account_id])