from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    telegram_id: str
    username: str | None = None
    first_name: str | None = None


class UserResponse(BaseModel):
    id: int
    telegram_id: str
    username: str | None
    first_name: str | None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
