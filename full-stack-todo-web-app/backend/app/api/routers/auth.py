from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from datetime import timedelta
import hashlib

from app.database.session import get_session
from app.models.user import User, UserCreate, UserPublic
from app.core.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/api/auth", tags=["authentication"])

def hash_password(password: str) -> str:
    """Simple password hashing using SHA256 - use bcrypt in production"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password

@router.post("/register")
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=hash_password(user_data.password)
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Create JWT token
    token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }

@router.post("/login")
def login_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """Login an existing user"""
    # Find user by email
    user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create JWT token
    token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name
        }
    }

@router.get("/me")
def get_current_user(session: Session = Depends(get_session)):
    """Get current user info - requires auth middleware to set user"""
    # This endpoint would typically use the user from the request context
    # For now, return a placeholder - the frontend uses JWT verification
    return {"message": "Use JWT token to get user info"}
