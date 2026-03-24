from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.content_plan import ContentPlan
from app.schemas.content_plan import ContentPlanCreate, ContentPlanResponse

router = APIRouter(prefix="/api/content-plans", tags=["content-plans"])


@router.get("/", response_model=list[ContentPlanResponse])
def list_content_plans(db: Session = Depends(get_db)):
    return db.query(ContentPlan).all()


@router.get("/{plan_id}", response_model=ContentPlanResponse)
def get_content_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(ContentPlan).filter(ContentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Content plan not found")
    return plan


@router.post("/", status_code=201, response_model=ContentPlanResponse)
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


@router.delete("/{plan_id}", status_code=204)
def delete_content_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(ContentPlan).filter(ContentPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Content plan not found")
    db.delete(plan)
    db.commit()
