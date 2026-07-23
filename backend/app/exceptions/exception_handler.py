from datetime import datetime

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError




async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "code": exc.status_code,
            "message": exc.detail,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )




async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "code": 422,
            "message": "Validation Error",
            "errors": exc.errors(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )




async def internal_server_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "code": 500,
            "message": str(exc),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )