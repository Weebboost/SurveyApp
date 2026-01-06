from sqlmodel import Session
from ...models.user import User
from ..repositories.user_repository import get_user_by_email
from ...core.password_hashing import verify_password
from ...core.exceptions import UnauthorizedError


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    if user.email_confirmed is False:
        raise UnauthorizedError("Email not confirmed")
    if user.is_active is False:
        raise UnauthorizedError("User is not active")
    return user