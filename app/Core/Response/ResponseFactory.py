from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any

from .APIResponse import APIResponse


class ResponseFactory:

    @staticmethod
    def Ok(data: Any = None, message: str | None = None):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=APIResponse(
                Success=True,
                Data=data,
                Message=message,
            ).model_dump(),
        )

    @staticmethod
    def Created(data: Any):
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=APIResponse(
                Success=True,
                Data=data,
            ).model_dump(),
        )

    @staticmethod
    def BadRequest(message: str):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=APIResponse(
                Success=False,
                Message=message,
            ).model_dump(),
        )

    @staticmethod
    def Unauthorized(message: str = "Unauthorized"):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=APIResponse(
                Success=False,
                Message=message,
            ).model_dump(),
        )

    @staticmethod
    def Forbidden(message: str = "Forbidden"):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=APIResponse(
                Success=False,
                Message=message,
            ).model_dump(),
        )

    @staticmethod
    def NotFound(message: str = "Not found"):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=APIResponse(
                Success=False,
                Message=message,
            ).model_dump(),
        )
