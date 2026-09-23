from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, database

router = APIRouter(
    prefix="/api/findings",
    tags=["Findings"]
)

@router.post("/{assessment_id}", response_model=schemas.FindingResponse)
def add_finding(assessment_id: int, finding: schemas.FindingCreate, db: Session = Depends(database.get_db)):
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    db_finding = models.Finding(**finding.model_dump(), assessment_id=assessment_id)
    db.add(db_finding)
    db.commit()
    db.refresh(db_finding)
    return db_finding

@router.get("/assessment/{assessment_id}", response_model=List[schemas.FindingResponse])
def get_findings_for_assessment(assessment_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Finding).filter(models.Finding.assessment_id == assessment_id).all()

@router.post("/{finding_id}/evidence", response_model=schemas.EvidenceResponse)
def add_evidence(finding_id: int, evidence: schemas.EvidenceCreate, db: Session = Depends(database.get_db)):
    finding = db.query(models.Finding).filter(models.Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
        
    db_evidence = models.Evidence(**evidence.model_dump(), finding_id=finding_id)
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence
