from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app import models, database, auth

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)

class OrderCreate(BaseModel):
    total_amount: float

class OrderResponse(OrderCreate):
    id: int
    customer_id: int
    status: str
    class Config:
        from_attributes = True

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    db_order = models.Order(**order.model_dump(), customer_id=current_user.id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Get order details.
    VULNERABLE: Broken Object Level Authorization (BOLA).
    Checks that the user is authenticated, but NOT if the order belongs to them.
    """
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
        
    # SECURE IMPLEMENTATION WOULD BE:
    # if order.customer_id != current_user.id and current_user.role != models.UserRole.admin:
    #     raise HTTPException(status_code=403, detail="Not authorized")
    
    return order
