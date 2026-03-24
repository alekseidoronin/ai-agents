from datetime import datetime

from pydantic import BaseModel


class SalesFunnelCreate(BaseModel):
    product_name: str
    funnel_type: str = "standard"
    target_audience: str


class SalesFunnelResponse(BaseModel):
    id: int
    user_id: int
    product_name: str | None
    funnel_type: str | None
    stages: list | None
    target_audience: str | None
    budget_recommendation: str | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}
