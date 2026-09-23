from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database, auth

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """Get the current authenticated user's profile."""
    return current_user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Get a specific user's profile.
    Intentionally vulnerable to BOLA in the lab version? We will implement that later.
    For now, just a standard endpoint.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

@router.put("/{user_id}/role", response_model=schemas.UserResponse)
def update_user_role(user_id: int, role: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Update a user's role.
    Intentionally vulnerable: Missing Admin-only check (Broken Function Level Authorization).
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    try:
        user.role = models.UserRole(role)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")
        
    db.commit()
    db.refresh(user)
    
    # Log the action
    log = models.AuditLog(user_id=current_user.id, action=f"UPDATE_ROLE_{role}", endpoint=f"/api/users/{user_id}/role")
    db.add(log)
    db.commit()
    
    return user
