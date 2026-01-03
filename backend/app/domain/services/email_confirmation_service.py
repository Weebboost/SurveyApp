from ...core.auth import decode_jwt_token
from .user_service import activate_and_confirm_user
from sqlmodel import Session
from ..repositories.user_repository import get_user_by_id

async def confirm_email(*, session: Session, token: str):
    token_data = decode_jwt_token(token)

    if token_data.sub is not None:
        user = get_user_by_id(session, token_data.sub)
        activate_and_confirm_user(session=session, user=user)