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



class Plans(Base):

    __tablename__ = 'plans'

    id                          = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
