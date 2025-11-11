from fastapi import APIRouter, Depends
from ..models.user import User
from ..models.survey import SurveyPublic, SurveyCreate
from ..core.db import get_session
from sqlmodel import Session
from fastapi import APIRouter, Depends, HTTPException
from ..core.db import get_session
from sqlmodel import Session
from fastapi import APIRouter, Depends
from typing import Annotated
from ..core.auth import get_current_user, get_superuser
from ..logic import survey_crud

router = APIRouter (
    prefix = "/survey",
    tags = ["survey"]
)

@router.post("/")
def create_survey(*, session: Session = Depends(get_session), user: Annotated[User, Depends(get_current_user)], survey_create: SurveyCreate):
    survey_crud.create_survey(session=session, user_id=user.id, survey_create=survey_create)


@router.get("/", response_model = list[SurveyPublic])
def get_all_user_surveys(*, session: Session = Depends(get_session), user: Annotated[User, Depends(get_current_user)]):
    return survey_crud.get_all_user_surveys(session=session, user_id=user.id)


@router.get("/{name}", response_model=list[SurveyPublic])
def get_survey_by_name(*, session: Session = Depends(get_session), user: Annotated[User, Depends(get_current_user)], name: str):
    surveys = survey_crud.get_survey_by_name(session=session, name=name)
    return [survey for survey in surveys if survey.user_id == user.id]