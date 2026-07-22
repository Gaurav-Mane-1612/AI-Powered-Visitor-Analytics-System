from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from backend.app.auth.jwt_handler import verify_access_token


class JWTBearer(HTTPBearer):

    async def __call__(self, request: Request):

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials is None:

            raise HTTPException(
                status_code=401,
                detail="Authentication Required"
            )

        if credentials.scheme != "Bearer":

            raise HTTPException(
                status_code=401,
                detail="Invalid Authentication Scheme"
            )

        payload = verify_access_token(credentials.credentials)

        if payload is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid or Expired Token"
            )

        return payload