from fastapi import APIRouter, Depends
from ..models.question import QuestionPublic, QuestionCreate
from ..core.db import get_session
from sqlmodel import Session
from ..logic.service import question_service
from ..models.user import User

from ..core.auth import get_current_user
from ..logic.policies import survey_owner_required
import uuid


router = APIRouter (
    prefix = "/question",
    tags = ["question"]
)


@router.post("/{survey_id}/", response_model = list[QuestionPublic])
def create_or_update_questions_for_survey(*, 
                                session: Session = Depends(get_session),  
                                questions: list[QuestionCreate],  
                                survey = Depends(survey_owner_required)
                                ):
    return question_service.create_or_update_questions_for_survey(session=session, questions=questions, survey_id=survey.id)

    
@router.get("/{survey_id}/", response_model=list[QuestionPublic])
def get_all_survey_questions(*, 
                             session: Session = Depends(get_session),  
                             survey = Depends(survey_owner_required)):
    return question_service.get_all_survey_questions(session=session, survey_id=survey.id)


