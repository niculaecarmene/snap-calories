"""
Main FastAPI application for SnapCalories.
WhatsApp-based nutrition tracking via AI vision.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api import health, webhooks

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info(f"Starting SnapCalories API in {settings.environment} mode")
    logger.info(f"Max image size: {settings.max_image_size_mb}MB")
    logger.info(f"Response timeout: {settings.response_timeout_seconds}s")
    yield
    # Shutdown
    logger.info("Shutting down SnapCalories API")


# Initialize FastAPI application
app = FastAPI(
    title="SnapCalories API",
    description="WhatsApp-based nutrition tracking powered by AI vision",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.is_development else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(webhooks.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.is_development
    )
