from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List, Dict, Any

T = TypeVar('T')

class StandardResponse(BaseModel, Generic[T]):
    """
    Standard response format for API endpoints
    """
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """
    Standard error response format
    """
    success: bool = False
    error: str
    message: Optional[str] = None

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response format
    """
    success: bool = True
    data: List[T]
    total: int
    page: int
    size: int
    pages: int