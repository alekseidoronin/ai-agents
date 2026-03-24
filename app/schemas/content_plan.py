from datetime import datetime

from pydantic import BaseModel


class ContentPlanCreate(BaseModel):
    product_name: str
    target_audience: str


class ContentPlanResponse(BaseModel):
    id: int
    user_id: int
    product_name: str | None
    target_audience: str | None
    topics: list | None
    schedule: dict | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
