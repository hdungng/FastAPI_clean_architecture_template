from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any

from .APIResponse import APIResponse, PagedResult


class ResponseFactory:

    @staticmethod
    def _create_response(
        success: bool,
        status_code: int,
        data: Any = None,
        message: str | None = None,
        meta: dict | None = None,
    ) -> JSONResponse:
        response_meta = meta or {}

        if isinstance(data, PagedResult):
            pagination = {
                "page": data.page,
                "pageSize": data.page_size,
                "total": data.total,
            }
            response_meta = {**response_meta, "pagination": pagination}
            data = data.items

        return JSONResponse(
            status_code=status_code,
            content=APIResponse(
                success=success,
                data=data,
                message=message,
                meta=response_meta,
            ).model_dump(),
        )

    @staticmethod
    def Ok(data: Any = None, message: str | None = "OK", meta: dict | None = None):
        return ResponseFactory._create_response(
            success=True,
            status_code=status.HTTP_200_OK,
            data=data,
            message=message,
            meta=meta,
        )

    @staticmethod
    def Created(data: Any, meta: dict | None = None):
        return ResponseFactory._create_response(
            success=True,
            status_code=status.HTTP_201_CREATED,
            data=data,
            meta=meta,
        )

    @staticmethod
    def BadRequest(message: str, meta: dict | None = None):
        return ResponseFactory._create_response(
            success=False,
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            meta=meta,
        )

    @staticmethod
    def Unauthorized(message: str = "Unauthorized", meta: dict | None = None):
        return ResponseFactory._create_response(
            success=False,
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            meta=meta,
        )

    @staticmethod
    def Forbidden(message: str = "Forbidden", meta: dict | None = None):
        return ResponseFactory._create_response(
            success=False,
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            meta=meta,
        )

    @staticmethod
    def NotFound(message: str = "Not found", meta: dict | None = None):
        return ResponseFactory._create_response(
            success=False,
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            meta=meta,
        )
