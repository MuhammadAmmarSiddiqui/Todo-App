"""
Logging configuration for the FastAPI application.

This module sets up comprehensive logging for authentication failures
and other security-related events.
"""

import logging
import os
from datetime import datetime
from typing import Optional

from fastapi import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send


def setup_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Configure authentication logger
    auth_logger = logging.getLogger("auth")
    auth_logger.setLevel(logging.INFO)

    # Create file handler for authentication events
    auth_handler = logging.FileHandler(f"{logs_dir}/auth.log")
    auth_handler.setLevel(logging.INFO)

    # Create console handler for authentication events
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    auth_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    auth_logger.addHandler(auth_handler)
    auth_logger.addHandler(console_handler)

    # Prevent propagation to root logger to avoid duplicate logs
    auth_logger.propagate = False

    return auth_logger


def log_auth_failure(
    event_type: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    reason: Optional[str] = None,
    request_path: Optional[str] = None
):
    """
    Log authentication failures and security events.

    Args:
        event_type: Type of security event (e.g., "INVALID_TOKEN", "USER_ID_MISMATCH")
        user_id: User ID involved in the event (if available)
        ip_address: IP address of the request
        user_agent: User agent string
        reason: Reason for the failure
        request_path: Request path that triggered the event
    """
    logger = logging.getLogger("auth")

    log_message = (
        f"SECURITY EVENT: {event_type} | "
        f"User ID: {user_id or 'N/A'} | "
        f"IP: {ip_address or 'N/A'} | "
        f"Path: {request_path or 'N/A'} | "
        f"Reason: {reason or 'N/A'} | "
        f"User Agent: {user_agent or 'N/A'}"
    )

    logger.warning(log_message)


def log_auth_success(
    user_id: str,
    ip_address: Optional[str] = None,
    request_path: Optional[str] = None
):
    """
    Log successful authentications.

    Args:
        user_id: User ID that was authenticated
        ip_address: IP address of the request
        request_path: Request path that was accessed
    """
    logger = logging.getLogger("auth")

    log_message = (
        f"AUTH SUCCESS: User {user_id} accessed {request_path or 'N/A'} "
        f"from IP {ip_address or 'N/A'}"
    )

    logger.info(log_message)


class LoggingMiddleware:
    """
    Middleware to log authentication-related events and security incidents.
    """
    def __init__(self, app: ASGIApp):
        self.app = app
        setup_logging()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        path = request.url.path

        # Only log for API routes
        if path.startswith("/api/"):
            # Capture client IP
            client_ip = request.client.host if request.client else None

            # Capture user agent
            user_agent = request.headers.get("user-agent", "N/A")

            # Log the request (before processing)
            auth_logger = logging.getLogger("auth")
            auth_logger.info(f"REQUEST: {request.method} {path} from {client_ip}")

        # Call the next middleware/route handler
        response_sent = False

        async def custom_send(message: Message) -> None:
            nonlocal response_sent
            if message["type"] == "http.response.start":
                # Log response status for API routes
                status_code = message["status"]
                if path and path.startswith("/api/") and status_code in [401, 403]:
                    auth_logger = logging.getLogger("auth")
                    if status_code == 401:
                        auth_logger.warning(f"401 UNAUTHORIZED: {request.method} {path} from {client_ip}")
                    elif status_code == 403:
                        auth_logger.warning(f"403 FORBIDDEN: {request.method} {path} from {client_ip}")

            await send(message)
            if message["type"] == "http.response.body":
                response_sent = True

        await self.app(scope, receive, custom_send)


# Initialize the logger when module is imported
setup_logging()