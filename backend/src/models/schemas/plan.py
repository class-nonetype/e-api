from pydantic import (BaseModel, ConfigDict)
from uuid import UUID

class Plan(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_account_id: UUID