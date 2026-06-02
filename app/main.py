from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .routers import auth, tasks
from .core.database import engine, Base
from .services.notification_service import NotificationService

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management System",
    description="A secure task management system with JWT authentication",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An internal error occurred",
            "error": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {
        "success": True,
        "message": "Welcome to Task Management System API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
def health_check():
    return {
        "success": True,
        "message": "Service is healthy",
        "timestamp": datetime.now().isoformat()
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize notification scheduler
    NotificationService.get_scheduler()
    print("Notification scheduler started")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    scheduler = NotificationService.get_scheduler()
    if scheduler:
        scheduler.shutdown()
        print("Notification scheduler shut down")