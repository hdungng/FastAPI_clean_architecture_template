from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.Core.Middleware import LoggingMiddleware, RequestIdMiddleware
from app.Modules.Users.UserController import router as UserRouter
from app.Modules.Auth.AuthController import router as AuthRouter
from app.Core.AppException import AppException
from app.Core.Response import ResponseFactory
from app.logging.Logger import configure_logging




def CreateApp() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="FastAPI Clean Modular",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Middleware
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(UserRouter, prefix="/api/v1")
    app.include_router(AuthRouter, prefix="/api/v1")

    # Exception handlers
    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(request, exc: RequestValidationError):
        errors: dict[str, list[str]] = {}
        for error in exc.errors():
            loc_parts = [
                str(part)
                for part in error.get("loc", [])
                if str(part) not in {"body", "query", "path", "header", "cookie"}
            ]
            field_name = ".".join(loc_parts) if loc_parts else "non_field_error"
            field_key = field_name[0].lower() + field_name[1:] if field_name else "field"
            errors.setdefault(field_key, []).append(error.get("msg", "Invalid input"))

        meta = {"errorCode": "VALIDATION_ERROR", "errors": errors}
        return ResponseFactory.BadRequest("Dữ liệu không hợp lệ", meta=meta)

    @app.exception_handler(AppException)
    async def handle_app_exception(request, exc: AppException):
        meta = {"errorCode": "APPLICATION_ERROR"}
        return ResponseFactory.BadRequest(str(exc), meta=meta)

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request, exc: HTTPException):
        meta = {
            "errorCode": "HTTP_ERROR",
            "statusCode": exc.status_code,
        }
        return ResponseFactory._create_response(
            success=False,
            status_code=exc.status_code,
            message=str(exc.detail) if exc.detail else exc.__class__.__name__,
            meta=meta,
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_exception(request, exc: Exception):
        meta = {"errorCode": "INTERNAL_SERVER_ERROR"}
        return ResponseFactory._create_response(
            success=False,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            meta=meta,
        )

    # Health check (no auth)
    @app.get("/health", tags=["System"])
    async def Health():
        return {"status": "ok"}

    return app


app = CreateApp()
