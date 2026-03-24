from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.content_plan import ContentPlan

router = APIRouter(prefix="/api/content-plans", tags=["content-plans"])


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

    model_config = {"from_attributes": True}


@router.get("/")
def list_content_plans(db: Session = Depends(get_db)):
    return db.query(ContentPlan).all()


@router.get("/{plan_id}")
def get_content_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(ContentPlan).filter(ContentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Content plan not found")
    return plan


@router.post("/", status_code=201)
def create_content_plan(
    payload: ContentPlanCreate,
    db: Session = Depends(get_db),
):
    plan = ContentPlan(
        user_id=1,
        product_name=payload.product_name,
        target_audience=payload.target_audience,
        topics=[],
        schedule={},
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan
