from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models import FindingSeverity, FindingStatus

# --- Evidence ---
class EvidenceBase(BaseModel):
    description: str
    request_payload: Optional[str] = None
    response_payload: Optional[str] = None
    screenshot_url: Optional[str] = None

class EvidenceCreate(EvidenceBase):
    pass

class EvidenceResponse(EvidenceBase):
    id: int
    finding_id: int
    class Config:
        from_attributes = True

# --- Finding ---
class FindingBase(BaseModel):
    title: str
    description: str
    severity: FindingSeverity
    status: FindingStatus = FindingStatus.open
    impact: Optional[str] = None
    remediation: Optional[str] = None
    cvss_score: Optional[str] = None

class FindingCreate(FindingBase):
    pass

class FindingResponse(FindingBase):
    id: int
    assessment_id: int
    created_at: datetime
    evidences: List[EvidenceResponse] = []
    class Config:
        from_attributes = True

# --- Assessment ---
class AssessmentBase(BaseModel):
    target_name: str
    description: Optional[str] = None
    status: str = "In Progress"

class AssessmentCreate(AssessmentBase):
    pass

class AssessmentResponse(AssessmentBase):
    id: int
    start_date: datetime
    end_date: Optional[datetime] = None
    findings: List[FindingResponse] = []
    class Config:
        from_attributes = True
