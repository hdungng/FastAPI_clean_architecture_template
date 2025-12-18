import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Callable, Optional

from app.Config.Settings import get_settings
from app.Core.CurrentUser import CurrentUser

security = HTTPBearer()


def Authorize(Role: Optional[str] = None) -> Callable:

    async def _Authorize(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        Settings = Depends(get_settings),
    ) -> CurrentUser:

        token = credentials.credentials

        try:
            payload = jwt.decode(
                token,
                Settings.jwt_secret,
                algorithms=["HS256"],
            )

            user_id = payload.get("sub")
            role = payload.get("role")

            if not user_id or not role:
                raise Exception()

            if Role and role != Role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Forbidden",
                )

            return CurrentUser(
                Id=int(user_id),
                Role=role,
            )

        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )

    return _Authorize
