import os
from dotenv import load_dotenv

# Load environment variables at the very beginning
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated

from app.database.session import get_session, engine
from app.models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from app.models.user import User
from app.core.auth import verify_jwt_token
from app.schemas.response import StandardResponse
from app.api.routers import tasks, auth
from app.api.routes import chat, chatkit
from app.core.middleware import AuthMiddleware
from app.core.logging_config import LoggingMiddleware

app = FastAPI(
    title="Todo API",
    description="Backend API for multi-user todo web application",
    version="1.0.0"
)

# Add logging middleware first
app.add_middleware(LoggingMiddleware)

# Add authentication middleware next (before CORS)
app.add_middleware(AuthMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks.router, prefix="/api/{user_id}", tags=["tasks"])
app.include_router(auth.router)
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(chatkit.router, prefix="/api", tags=["chatkit"]) # ChatKit integration

@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Todo API Backend"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}