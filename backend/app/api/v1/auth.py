from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ...models.token import Token
from ...core.db import get_session
from sqlmodel import Session
from ...core.auth import create_token
from ...domain.services.auth_service import authenticate_user
from datetime import timedelta
from ...core.config import settings
from ...domain.auth import email_confirmation
from ...domain.auth import password_confirmation
from ..schemas.auth import EmailRequest, PasswordResetConfirmRequest


router = APIRouter(
    prefix="/auth",
    tags=["auth"])


@router.post("/token")
async def login_for_access_token(*, session: Session = Depends(get_session), form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
            )
    return Token(access_token=create_token(user.id, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)))


@router.post("/email/confirmation")
async def confirm_email(*, session: Session = Depends(get_session), data: EmailRequest):
    await email_confirmation.complete_email_confirmation(session=session, token=data.token)


@router.post("/email/send-confirmation-mail")
async def send_confirmation_email(*, session: Session = Depends(get_session), email: str):
    await email_confirmation.initiate_email_confirmation(session=session, email=email)


@router.post("/password/reset")
async def reset_password(*, session: Session = Depends(get_session), data: PasswordResetConfirmRequest):
    await password_confirmation.complete_password_reset(session=session, token=data.token, new_password=data.new_password)


@router.post("/password/send-reset-mail")
async def send_password_reset_email(*, session: Session = Depends(get_session), email: str):
    await password_confirmation.initiate_password_reset(session=session, email=email)