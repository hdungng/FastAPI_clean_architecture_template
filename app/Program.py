from fastapi import FastAPI

from app.Core.Middleware import RequestIdMiddleware
from app.Modules.Users.UserController import router as UserRouter
from app.Modules.Auth.AuthController import router as AuthRouter
from fastapi.responses import JSONResponse
from app.Core.AppException import AppException
from app.Core.Response.APIResponse import APIResponse




def CreateApp() -> FastAPI:
    app = FastAPI(
        title="FastAPI Clean Modular",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Middleware
    app.add_middleware(RequestIdMiddleware)

    # Routers
    app.include_router(UserRouter, prefix="/api/v1")
    app.include_router(AuthRouter, prefix="/api/v1")

    # Health check (no auth)
    @app.get("/health", tags=["System"])
    async def Health():
        return {"status": "ok"}

    return app


app = CreateApp()
