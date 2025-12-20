from fastapi import Depends
from sqlalchemy.orm import Session
from ..core.db import get_session
from ..core.auth import get_current_user
from ..models.user import User
from ..core.exceptions import NotFoundError, NotOwnerError
from .crud.survey_crud import get_survey_by_id
import uuid
from ..core.transaction import transactional

@transactional()
def survey_owner_required(*, session: Session = Depends(get_session), user: User = Depends(get_current_user), survey_id: uuid.UUID):
    survey = get_survey_by_id(session, survey_id)
    return survey
