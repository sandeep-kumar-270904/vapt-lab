from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class FindingSeverity(str, enum.Enum):
    critical = "Critical"
    high = "High"
    medium = "Medium"
    low = "Low"
    informational = "Informational"

class FindingStatus(str, enum.Enum):
    open = "Open"
    remediated = "Remediated"
    accepted_risk = "Accepted Risk"
    false_positive = "False Positive"

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    target_name = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, default="In Progress")

    findings = relationship("Finding", back_populates="assessment")

class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(FindingSeverity), nullable=False)
    status = Column(Enum(FindingStatus), default=FindingStatus.open)
    impact = Column(Text)
    remediation = Column(Text)
    cvss_score = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    assessment = relationship("Assessment", back_populates="findings")
    evidences = relationship("Evidence", back_populates="finding")

class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True, index=True)
    finding_id = Column(Integer, ForeignKey("findings.id"))
    description = Column(String)
    request_payload = Column(Text)
    response_payload = Column(Text)
    screenshot_url = Column(String, nullable=True)
    
    finding = relationship("Finding", back_populates="evidences")
