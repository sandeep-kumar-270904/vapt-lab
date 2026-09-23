from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database, schemas

router = APIRouter(
    prefix="/api/remediation",
    tags=["Remediation"]
)

@router.put("/{finding_id}/status", response_model=schemas.FindingResponse)
def update_finding_status(finding_id: int, status: str, db: Session = Depends(database.get_db)):
    """Update finding status for tracking remediation and retesting."""
    finding = db.query(models.Finding).filter(models.Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
        
    try:
        finding.status = models.FindingStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    db.commit()
    db.refresh(finding)
    return finding
