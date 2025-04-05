from uuid import UUID

from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserComment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_account_id: UUID
    full_name: str
    text: str
    public: bool
    

class CreateUserComment(UserComment):
    pass


class ModifyUserComment(BaseModel):
    text: str

class DeleteUserComment(BaseModel):
    user_comment_id: UUID