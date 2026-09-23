from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from pydantic import BaseModel
from app import models, database, auth

router = APIRouter(
    prefix="/api/products",
    tags=["Products"]
)

class ProductCreate(BaseModel):
    name: str
    description: str = None
    price: float
    stock: int = 0

class ProductResponse(ProductCreate):
    id: int
    seller_id: int
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ProductResponse])
def list_products(search: str = None, db: Session = Depends(database.get_db)):
    """List products."""
    if search:
        # SECURE: Using ORM which parameterizes queries automatically
        return db.query(models.Product).filter(models.Product.name.ilike(f"%{search}%")).all()
    else:
        return db.query(models.Product).all()

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """Create a product. Should be seller or admin."""
    if current_user.role == models.UserRole.customer:
        raise HTTPException(status_code=403, detail="Not authorized to create products")
        
    db_product = models.Product(**product.model_dump(), seller_id=current_user.id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    return db_product

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
