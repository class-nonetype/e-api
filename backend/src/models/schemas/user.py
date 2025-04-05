from pydantic import (BaseModel, ConfigDict)
from uuid import UUID
from typing import Optional

from src.models.schemas.plan import Plan

class UserSession(BaseModel):
    client: str
    user_full_name: str
    user_id: int
    access_token: str
    views_control_access: list[str]



class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str
    e_mail: str


class UserAccount(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    password: str



class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    UserAccount: UserAccount
    UserProfile: UserProfile





class CreateUserAccount(User):
    pass
