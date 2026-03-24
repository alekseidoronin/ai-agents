from datetime import datetime

from pydantic import BaseModel


class AgentSessionResponse(BaseModel):
    id: int
    user_id: int
    agent_type: str
    status: str
    context: dict | None
    result: dict | None
    created_at: datetime
    finished_at: datetime | None

    model_config = {"from_attributes": True}
