from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from app import models, database, auth

router = APIRouter(
    prefix="/api/reviews",
    tags=["Reviews"]
)

class ReviewCreate(BaseModel):
    product_id: int
    rating: int
    comment: str

class ReviewResponse(ReviewCreate):
    id: int
    user_id: int
    class Config:
        from_attributes = True

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: ReviewCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Create a review.
    VULNERABLE: No sanitization of the 'comment' field. Stores raw input that can be executed as XSS on the frontend.
    """
    db_review = models.Review(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/{product_id}", response_model=List[ReviewResponse])
def get_product_reviews(product_id: int, db: Session = Depends(database.get_db)):
    reviews = db.query(models.Review).filter(models.Review.product_id == product_id).all()
    return reviews
