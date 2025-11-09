from fastapi import APIRouter, Depends
from ..models.user import UserCreate, User, UserPublic
from ..core.db import get_session
from ..logic import user_crud
from sqlmodel import Session
from fastapi import APIRouter, Depends
from typing import Annotated
from ..core.auth import get_current_user, get_superuser

router = APIRouter (
    prefix = "/user",
    tags = ["user"]
)

@router.get("/all_users", response_model=list[UserPublic])
def get_users(*, session: Session = Depends(get_session),  user: Annotated[User, Depends(get_superuser)]):
    return user_crud.get_users(session)


@router.get("/")
def get_user(*, user: Annotated[User, Depends(get_current_user)]):
    return user


@router.post("/")
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    return user_crud.create_user(session,user)


@router.delete("/")
def delete_user(*, session: Session = Depends(get_session), user: Annotated[User, Depends(get_current_user)]):
    user_crud.delete_user(session, user)
