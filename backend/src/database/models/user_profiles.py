from uuid import uuid4

from src.config.utils import get_datetime
from src.database.base import base as Base

from sqlalchemy import (
    Column,
    String,
    DateTime
)
from sqlalchemy.dialects.postgresql import UUID

class UserProfiles(Base):
    __tablename__           = 'user_profiles'

    id                      = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    full_name               = Column(String, nullable=True)
    e_mail                  = Column(String, nullable=False)
    creation_date           = Column(DateTime, default=lambda: get_datetime())
    modification_date       = Column(DateTime, nullable=True, default=lambda: get_datetime())
    
