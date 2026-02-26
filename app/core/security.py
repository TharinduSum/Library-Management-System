from datetime import datetime, timedelta, timezone
import hashlib
from typing import Any, Dict

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    hashed_password_enc = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_byte_enc, hashed_password_enc)


# Backwards-compatible alias
get_password_hash = hash_password


def _create_token(
    data: Dict[str, Any],
    expires_delta: timedelta,
    token_type: str,
) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta
    to_encode.update({"exp": expire, "iat": now, "type": token_type})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def create_access_token(data: Dict[str, Any]) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(data, expires_delta, token_type="access")


def create_refresh_token(data: Dict[str, Any]) -> str:
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(data, expires_delta, token_type="refresh")


def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError as exc:
        raise ValueError("Invalid token") from exc


def generate_api_key() -> tuple[str, str]:
    """Return (raw_key_with_prefix, key_hash)."""
    # 32 bytes random -> hex string
    raw = hashlib.sha256(hashlib.token_bytes(32)).hexdigest()
    raw_with_prefix = f"{settings.API_KEY_PREFIX}{raw}"
    key_hash = hash_api_key(raw_with_prefix)
    return raw_with_prefix, key_hash


def hash_api_key(raw_key_with_prefix: str) -> str:
    """Stable hash of the full API key (including prefix)."""
    return hashlib.sha256(raw_key_with_prefix.encode("utf-8")).hexdigest()
