from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import auth, users

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MarketHub API",
    description="Authorized Web & API VAPT Engagement Lab",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MarketHub API Lab"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
