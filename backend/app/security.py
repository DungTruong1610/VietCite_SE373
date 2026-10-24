"""Authentication for the web app: two roles (editor, approver), JWT bearer tokens.

Phase 1 keeps users in memory, seeded from the environment (never hard-coded in the repo):

    SEED_EDITOR_USERNAME   (default: editor)     SEED_EDITOR_PASSWORD
    SEED_APPROVER_USERNAME (default: approver)   SEED_APPROVER_PASSWORD

A user whose password variable is empty is not created. With no user at all, ``/api/auth/login``
answers 503 and says which variables to set. Passwords are stored as PBKDF2-SHA256 hashes and
compared in constant time. Five failed logins lock a username for five minutes.

``JWT_SECRET`` signs tokens. When it is empty (local dev), a random secret is generated per process:
tokens then stop working after a restart, and a warning is logged.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import secrets
import threading
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Annotated, Literal

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from geo.config import get_settings

log = logging.getLogger("vietcite.auth")

Role = Literal["editor", "approver"]
PBKDF2_ROUNDS = 240_000
TOKEN_TTL = timedelta(hours=8)
MAX_FAILURES = 5
LOCK_SECONDS = 300
ALGORITHM = "HS256"


@dataclass(frozen=True)
class User:
    username: str
    role: Role
    salt: bytes
    password_hash: bytes


def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS)


def _seed_users() -> dict[str, User]:
    users: dict[str, User] = {}
    for role, default_name in (("editor", "editor"), ("approver", "approver")):
        password = os.environ.get(f"SEED_{role.upper()}_PASSWORD", "")
        if not password:
            continue
        username = os.environ.get(f"SEED_{role.upper()}_USERNAME", default_name)
        salt = secrets.token_bytes(16)
        users[username] = User(username, role, salt, hash_password(password, salt))  # type: ignore[arg-type]
    return users


class AuthService:
    def __init__(self, users: dict[str, User], secret: str | None) -> None:
        self.users = users
        if not secret:
            log.warning("JWT_SECRET is empty: using a random per-process secret (tokens reset on restart)")
        self._secret = secret or secrets.token_hex(32)
        self._failures: dict[str, list[float]] = {}
        self._lock = threading.Lock()

    @property
    def configured(self) -> bool:
        return bool(self.users)

    def _locked(self, username: str) -> bool:
        now = time.monotonic()
        recent = [t for t in self._failures.get(username, []) if now - t < LOCK_SECONDS]
        self._failures[username] = recent
        return len(recent) >= MAX_FAILURES

    def authenticate(self, username: str, password: str) -> User | None:
        with self._lock:
            if self._locked(username):
                log.warning("login locked for a username after repeated failures")
                return None
            user = self.users.get(username)
            # Hash even for unknown users so timing does not reveal which usernames exist.
            salt = user.salt if user else b"\x00" * 16
            candidate = hash_password(password, salt)
            if user and hmac.compare_digest(candidate, user.password_hash):
                self._failures.pop(username, None)
                return user
            self._failures.setdefault(username, []).append(time.monotonic())
            log.warning("failed login attempt")
            return None

    def issue_token(self, user: User) -> str:
        now = datetime.now(UTC)
        claims = {"sub": user.username, "role": user.role, "iat": now, "exp": now + TOKEN_TTL}
        return jwt.encode(claims, self._secret, algorithm=ALGORITHM)

    def decode(self, token: str) -> User | None:
        try:
            claims = jwt.decode(token, self._secret, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            return None
        user = self.users.get(str(claims.get("sub")))
        return user if user and user.role == claims.get("role") else None


_service: AuthService | None = None


def get_auth_service() -> AuthService:
    global _service
    if _service is None:
        _service = AuthService(_seed_users(), get_settings().jwt_secret)
    return _service


def reset_auth_service() -> None:
    """Re-read seed users and secret (tests)."""
    global _service
    _service = None


_bearer = HTTPBearer(auto_error=False)


def current_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    auth: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    user = auth.decode(creds.credentials) if creds else None
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Chưa đăng nhập hoặc phiên đã hết hạn",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_role(role: Role):
    def dependency(user: Annotated[User, Depends(current_user)]) -> User:
        if user.role != role:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Cần vai trò {role}")
        return user

    return dependency
