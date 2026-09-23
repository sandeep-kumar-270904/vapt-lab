from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app import models, database
from datetime import datetime

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)

def generate_markdown_report(assessment: models.Assessment) -> str:
    md = []
    
    # Title Page
    md.append(f"# Web & API Security Assessment Report")
    md.append(f"**Target:** {assessment.target_name}")
    md.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}")
    md.append(f"**Status:** {assessment.status}")
    md.append("\n---\n")
    
    # Executive Summary
    md.append("## Executive Summary")
    if assessment.description:
        md.append(f"{assessment.description}\n")
    else:
        md.append("This report outlines the findings from the authorized security assessment.\n")
        
    # Finding Statistics
    critical = sum(1 for f in assessment.findings if f.severity.value == "Critical")
    high = sum(1 for f in assessment.findings if f.severity.value == "High")
    medium = sum(1 for f in assessment.findings if f.severity.value == "Medium")
    low = sum(1 for f in assessment.findings if f.severity.value == "Low")
    
    md.append("### Finding Summary")
    md.append(f"- **Critical:** {critical}")
    md.append(f"- **High:** {high}")
    md.append(f"- **Medium:** {medium}")
    md.append(f"- **Low:** {low}\n")
    md.append("---\n")
    
    # Detailed Findings
    md.append("## Detailed Findings\n")
    
    if not assessment.findings:
        md.append("*No findings recorded for this assessment.*")
        
    for index, finding in enumerate(assessment.findings, 1):
        md.append(f"### {index}. {finding.title}")
        md.append(f"**Severity:** {finding.severity.value} | **Status:** {finding.status.value}")
        if finding.cvss_score:
            md.append(f"**CVSS Score:** {finding.cvss_score}")
        md.append("\n**Description:**")
        md.append(f"{finding.description}\n")
        
        if finding.impact:
            md.append("**Impact:**")
            md.append(f"{finding.impact}\n")
            
        if finding.remediation:
            md.append("**Remediation:**")
            md.append(f"{finding.remediation}\n")
            
        if finding.evidences:
            md.append("**Evidence / Proof of Concept:**")
            for ev in finding.evidences:
                md.append(f"*{ev.description}*")
                if ev.request_payload:
                    md.append("```http")
                    md.append(ev.request_payload)
                    md.append("```")
                if ev.response_payload:
                    md.append("```http")
                    md.append(ev.response_payload)
                    md.append("```")
                md.append("\n")
                
        md.append("---\n")
        
    return "\n".join(md)


@router.get("/{assessment_id}/markdown", response_class=PlainTextResponse)
def get_markdown_report(assessment_id: int, db: Session = Depends(database.get_db)):
    """Generate a Markdown report for a specific assessment."""
    assessment = db.query(models.Assessment).filter(models.Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
        
    report = generate_markdown_report(assessment)
    return report
