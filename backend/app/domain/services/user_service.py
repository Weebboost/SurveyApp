from sqlmodel import Session
from ...models.user import User, UserCreate, UserUpdate
from ..repositories import user_repository
from ...core.transaction import transactional
from ...core.password_utils import hash_password
from datetime import datetime, timezone
from ...core.confirmation_mailer import confirmation

@transactional()
def get_users(*, session: Session) -> list[User]:
    return user_repository.get_users(session=session)

@transactional()
def create_user(*, session: Session, user_create: UserCreate) -> User:
    user = User.model_validate(
          user_create, 
          update = {
               "hashed_password": hash_password(user_create.password),
               "created_at": datetime.now(timezone.utc)
               }
          )

    new_user = user_repository.create_user(session=session, user=user)
    confirmation(user_id=new_user.id, user_mail=new_user.email)
    return new_user


@transactional()
def delete_user(*, session: Session, user: User):
    user_repository.delete_user(session=session, user=user)


@transactional()
def update_user(*, session: Session, user: User, user_update: UserUpdate):
    if user_update.email:
          user.email = user_update.email
    if user_update.password:
          user.hashed_password = hash_password(user_update.password)

    updated_user = user_repository.update_user(session=session, user=user)
    return updated_user

@transactional()
def activate_and_confirm_user(*, session: Session, user: User):
    user.is_active = True
    user.email_confirmed = True
    updated_user = user_repository.update_user(session=session, user=user)
    return updated_user