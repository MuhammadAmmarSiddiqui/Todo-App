"""
ChatKit API routes for handling ChatKit client requests.
"""

from fastapi import APIRouter, Request

router = APIRouter(prefix="/chatkit", tags=["chatkit"])


@router.post("/session")
async def create_chatkit_session():
    """
    Create a ChatKit session and return client secret.
    """
    # For the hackathon, we'll return a mock client secret that satisfies the SDK's format validation.
    # In a real OpenAI integration, this would involve calling the ChatKit API.
    return {
        "client_secret": "sess_mock_secret_for_gemini_backend_realignment",
        "status": "success"
    }


@router.post("/messages")
async def handle_chatkit_message(request: Request):
    """
    Handle incoming ChatKit messages.
    
    NOTE: Full ChatKit integration requires significant complexity.
    """
    return {
        "error": "ChatKit integration incomplete", 
        "message": "Consider using ChatScope UI Kit (@chatscope/chat-ui-kit-react) instead"
    }


@router.get("/health")
async def chatkit_health():
    """Health check endpoint"""
    return {
        "status": "partial",
        "chatkit_server": "placeholder",
        "backend": "gemini-2.0-flash",
        "note": "ChatKit integration is complex - consider ChatScope UI Kit alternative"
    }
