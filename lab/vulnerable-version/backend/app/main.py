from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import auth, users, products, orders, reviews

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MarketHub API",
    description="Authorized Web & API VAPT Engagement Lab",
    version="1.0.0"
)

# VULNERABLE: Security Misconfiguration - Wildcard CORS allows any origin to read responses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(reviews.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the MarketHub API Lab"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
