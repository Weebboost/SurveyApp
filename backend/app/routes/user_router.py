from fastapi import APIRouter, Depends
from ..models.user import UserCreate, User, UserPublic
from ..core.db import get_session
from ..logic import user_crud
from sqlmodel import Session

router = APIRouter (
    prefix = "/users",
    tags = ["users"]
)

@router.get("/", response_model=list[UserPublic])
def get_users(*, session: Session = Depends(get_session)):
    return user_crud.get_users(session)

@router.post("/")
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    user_crud.create_user(session,user)

@router.delete("/")
def delete_users(*, session: Session = Depends(get_session), user: User):
    user_crud.delete_user(session, user)