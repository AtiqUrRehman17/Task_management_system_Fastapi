import logging
from datetime import datetime, timezone

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, tasks
from .core.database import engine, Base
from .core.config import settings

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

# API Version Prefix
API_V1_PREFIX = "/api/v1"

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management System",
    description="A secure task management system with JWT authentication",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    """
    Global exception handler.

    Logs the complete exception internally but
    prevents leaking implementation details
    to API consumers.
    """

    logger.exception(
        f"Unhandled exception occurred. "
        f"Path={request.url.path}"
    )

    response = {
        "success": False,
        "message": "An internal server error occurred.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    # Show detailed errors only in development
    if settings.DEBUG:
        response["error"] = str(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response
    )


# Include routers
app.include_router(
    auth.router,
    prefix=API_V1_PREFIX
)

app.include_router(
    tasks.router,
    prefix=API_V1_PREFIX
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "Welcome to Task Management System API",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "Service is healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }