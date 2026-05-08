from datetime import UTC, datetime, timedelta
from uuid import NAMESPACE_URL, uuid5

import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, field_validator

from app.core.config import settings

router = APIRouter(prefix="/api/dev/auth", tags=["dev-auth"])


class DevSessionRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("Email is required")

        return normalized


class DevSessionUser(BaseModel):
    id: str
    email: str


class DevSessionResponse(BaseModel):
    accessToken: str
    user: DevSessionUser


@router.post("/session", response_model=DevSessionResponse, status_code=status.HTTP_201_CREATED)
def create_dev_session(request: DevSessionRequest) -> DevSessionResponse:
    if settings.app_env != "local":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    user_id = str(uuid5(NAMESPACE_URL, f"weizhi-local-dev:{request.email.lower()}"))
    token = jwt.encode(
        {
            "sub": user_id,
            "email": request.email,
            "aud": "authenticated",
            "iss": f"{settings.supabase_url.rstrip('/')}/auth/v1",
            "role": "authenticated",
            "exp": datetime.now(UTC) + timedelta(hours=8),
        },
        settings.supabase_jwt_secret,
        algorithm="HS256",
    )

    return DevSessionResponse(
        accessToken=token,
        user=DevSessionUser(id=user_id, email=request.email),
    )
