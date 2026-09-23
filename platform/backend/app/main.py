from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import assessments, findings, remediation

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="VAPT-Lab Assessment Platform API",
    description="Backend for tracking VAPT findings and generating reports",
    version="1.0.0"
)

# Secure CORS for the Platform
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"], # Assuming frontend runs on 5174
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assessments.router)
app.include_router(findings.router)
app.include_router(remediation.router)

@app.get("/")
def read_root():
    return {"message": "VAPT-Lab Platform API is running"}
