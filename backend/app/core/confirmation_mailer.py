from datetime import timedelta
import uuid
from .mail import send_confirmation_email
from .auth import create_token
from .config import settings

def confirmation(user_id: uuid.UUID, user_mail: str):
    token = create_token(subject=user_id, expires_delta=timedelta(minutes=settings.CONFIRMATION_TOKEN_EXPIRE_MINUTES))
    link = f"{settings.FRONTEND_URL}/auth/confirm-email?token={token}"
    send_confirmation_email(to_address=user_mail, confirmation_link=link)