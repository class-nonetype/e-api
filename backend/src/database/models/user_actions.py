from uuid import uuid4

from src.database.base import base as Base
from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.dialects.postgresql import UUID


class UserActions(Base):
    __tablename__       = 'user_actions'

    id                  = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    name                = Column(String, nullable=True)
