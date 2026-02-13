"""
Health check endpoints for monitoring application status.
"""
from fastapi import APIRouter
from datetime import datetime
from typing import Dict

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    Returns current status, timestamp, and version.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "SnapCalories",
        "version": "1.0.0"
    }


@router.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint with API information.
    """
    return {
        "service": "SnapCalories API",
        "description": "WhatsApp-based nutrition tracking via AI",
        "version": "1.0.0",
        "docs": "/docs"
    }
