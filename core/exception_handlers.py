from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi import Request, status
from fastapi.responses import JSONResponse
from core.settings import settings
from fastapi.exception_handlers import (
    http_exception_handler as fastapi_http_exception_handler,
    request_validation_exception_handler as fastapi_request_validation_exception_handler,
)

templates = settings.templates


async def general_exception_handler(request: Request, exc: Exception):
    print(
        f"General exception handler called for path: {request.url.path} with exception: {exc}"
    )
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )
    else:
        return templates.TemplateResponse(
            request,
            "500.html",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    print(
        f"HTTP exception handler called for path: {request.url.path} with status code: {exc.status_code}"
    )
    if request.url.path.startswith("/api"):
        return await fastapi_http_exception_handler(request, exc)
    elif exc.status_code == status.HTTP_404_NOT_FOUND:
        return templates.TemplateResponse(
            request, "404.html", status_code=status.HTTP_404_NOT_FOUND
        )
    elif exc.status_code == status.HTTP_403_FORBIDDEN:
        return templates.TemplateResponse(
            request, "403.html", status_code=status.HTTP_403_FORBIDDEN
        )
    else:
        return templates.TemplateResponse(
            request,
            "error.html",
            {"status_code": exc.status_code, "detail": exc.detail},
        )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(
        f"Validation exception handler called for path: {request.url.path} with errors: {exc.errors()}"
    )
    if request.url.path.startswith("/api"):
        return await fastapi_request_validation_exception_handler(request, exc)
    else:
        return templates.TemplateResponse(
            request,
            "validation_error.html",
            {"errors": exc.errors(), "body": exc.body},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
