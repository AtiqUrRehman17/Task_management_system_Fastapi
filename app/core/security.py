from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from .config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

MAX_BCRYPT_PASSWORD_LENGTH = 72


def _validate_password(password: str):
    if not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty"
        )

    if len(password.encode("utf-8")) > MAX_BCRYPT_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password too long (bcrypt max is 72 bytes). Please use a shorter password."
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password safely using bcrypt
    """
    try:
        _validate_password(plain_password)
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt
    """
    _validate_password(password)
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError:
        return None