from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from backend.app.database.database import get_connection

from backend.app.routes.visitor_routes import router as visitor_router
from backend.app.routes.visit_routes import router as visit_router
from backend.app.routes.dashboard_routes import router as dashboard_router
from backend.app.routes.feedback_routes import router as feedback_router
from backend.app.routes.user_routes import router as user_router
from backend.app.routes.audit_routes import router as audit_router

from backend.app.exceptions.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    internal_server_exception_handler
)

app = FastAPI(
    title="AI-Powered Visitor Analytics System",
    version="1.0.0",
    description="Backend API for AI-Powered Visitor Analytics System"
)

# ============================
# Exception Handlers
# ============================

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    internal_server_exception_handler
)

# ============================
# Routers
# ============================

app.include_router(visitor_router)
app.include_router(visit_router)
app.include_router(dashboard_router)
app.include_router(feedback_router)
app.include_router(user_router)
app.include_router(audit_router)

# ============================
# Root API
# ============================

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI-Powered Visitor Analytics System API is Running 🚀",
        "version": "1.0.0"
    }


# ============================
# Health Check
# ============================

@app.get("/health")
def health_check():

    try:

        connection = get_connection()
        connection.close()

        return {
            "status": "success",
            "database": "Connected"
        }

    except Exception as e:

        return {
            "status": "error",
            "database": "Disconnected",
            "message": str(e)
        }