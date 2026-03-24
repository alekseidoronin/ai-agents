from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sales_funnel import SalesFunnel
from app.schemas.sales_funnel import SalesFunnelCreate, SalesFunnelResponse

router = APIRouter(prefix="/api/sales-funnels", tags=["sales-funnels"])


@router.get("/", response_model=list[SalesFunnelResponse])
def list_sales_funnels(db: Session = Depends(get_db)):
    return db.query(SalesFunnel).all()


@router.get("/{funnel_id}", response_model=SalesFunnelResponse)
def get_sales_funnel(funnel_id: int, db: Session = Depends(get_db)):
    funnel = db.query(SalesFunnel).filter(SalesFunnel.id == funnel_id).first()
    if not funnel:
        raise HTTPException(status_code=404, detail="Sales funnel not found")
    return funnel


@router.post("/", status_code=201, response_model=SalesFunnelResponse)
def create_sales_funnel(
    payload: SalesFunnelCreate,
    db: Session = Depends(get_db),
):
    funnel = SalesFunnel(
        user_id=1,
        product_name=payload.product_name,
        funnel_type=payload.funnel_type,
        target_audience=payload.target_audience,
        stages=[],
    )
    db.add(funnel)
    db.commit()
    db.refresh(funnel)
    return funnel


@router.delete("/{funnel_id}", status_code=204)
def delete_sales_funnel(funnel_id: int, db: Session = Depends(get_db)):
    funnel = db.query(SalesFunnel).filter(SalesFunnel.id == funnel_id).first()
    if not funnel:
        raise HTTPException(status_code=404, detail="Sales funnel not found")
    db.delete(funnel)
    db.commit()
