from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter(
    prefix="/api/assessments",
    tags=["Assessments"]
)

@router.post("/", response_model=schemas.AssessmentResponse)
def create_assessment(assessment: schemas.AssessmentCreate, db: Session = Depends(database.get_db)):
    db_assessment = models.Assessment(**assessment.model_dump())
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

@router.get("/", response_model=List[schemas.AssessmentResponse])
def get_assessments(db: Session = Depends(database.get_db)):
    return db.query(models.Assessment).all()

@router.get("/{assessment_id}", response_model=schemas.AssessmentResponse)
def get_assessment(assessment_id: int, db: Session = Depends(database.get_db)):
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment
