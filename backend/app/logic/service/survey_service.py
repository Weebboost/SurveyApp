from ..crud import survey_crud_crud
from sqlmodel import Session
from ...models.survey import Survey, SurveyCreate
from sqlalchemy.exc import SQLAlchemyError
from ...core.exceptions import CouldNotCreateResource, NotFoundError, BaseException
from ..crud import survey_crud

import uuid 

def create_survey(*, session: Session, user_id: uuid.UUID, survey_create = SurveyCreate) -> Survey:
    try:
        survey = survey_crud.create_survey(session=session, user_id=user_id, survey_create=survey_create)
        session.commit()
        session.refresh(survey)

        return survey
    
    except SQLAlchemyError as e:
        session.rollback()
        raise CouldNotCreateResource(message="Database error while creating survey")
    
    except Exception as e:
        session.rollback()
        raise CouldNotCreateResource(message="Could not create survey due to unexpected error")
    

def get_all_user_surveys(session: Session, user_id: uuid.UUID) -> list[Survey]:
    try:
        return survey_crud.get_all_user_surveys(session=session, user_id=user_id)

    except SQLAlchemyError as e:
        raise CouldNotCreateResource(message="An error occurred while retrieving data from the database.")
    
    except Exception as e:
        raise CouldNotCreateResource(message="Could not retrive data due to unexpected error")
    

def get_survey_by_name(session: Session, name: str, user_id = uuid.UUID) -> list[Survey]:
    try:
        surveys = survey_crud.get_survey_by_name(session=session, name=name)
        return [survey for survey in surveys if survey.user_id == user_id]
    
    except SQLAlchemyError as e:
        raise CouldNotCreateResource(message="An error occurred while retrieving data from the database.")
    
    except Exception as e:
        raise CouldNotCreateResource(message="Could not retrive data due to unexpected error")
    

