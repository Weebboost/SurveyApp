from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from ..models.token import TokenPayload
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pydantic import ValidationError
from sqlmodel import Session
from .db import get_session
from ..models.user import User
from ..domain.repositories.user_repository import get_user_by_email, get_user_by_id
from ..core.password_utils import verify_password
from datetime import timedelta, datetime, timezone
from ..core.exceptions import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def decode_jwt_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp", "sub"]} 
        )
        return TokenPayload(**payload)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_token_payload(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenPayload:
    return decode_jwt_token(token)

    
async def get_current_user(*, session: Session = Depends(get_session), token_data: TokenPayload = Depends(get_token_payload)):
    user = get_user_by_id(session,token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise UnauthorizedError("User is not active")
    if user.email_confirmed is False:
        raise UnauthorizedError("Email not confirmed")
    return user


def get_superuser(user: Annotated[User, Depends(get_current_user)]):
    if user.role == "superuser":
        return user
    raise HTTPException(status_code=403, detail="You do not have permission to access this resource")


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    if user.email_confirmed is False:
        raise UnauthorizedError("Email not confirmed")
    if user.is_active is False:
        raise UnauthorizedError("User is not active")
    return user


def create_token(subject: str, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
