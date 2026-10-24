"""Login and current user."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.security import AuthService, Role, User, current_user, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=256)


class UserOut(BaseModel):
    username: str
    role: Role


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, auth: Annotated[AuthService, Depends(get_auth_service)]) -> LoginResponse:
    if not auth.configured:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Chưa cấu hình tài khoản: đặt SEED_EDITOR_PASSWORD và SEED_APPROVER_PASSWORD trong .env",
        )
    user = auth.authenticate(body.username, body.password)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Sai tên đăng nhập hoặc mật khẩu")
    return LoginResponse(
        access_token=auth.issue_token(user), user=UserOut(username=user.username, role=user.role)
    )


@router.get("/me", response_model=UserOut)
def me(user: Annotated[User, Depends(current_user)]) -> UserOut:
    return UserOut(username=user.username, role=user.role)
