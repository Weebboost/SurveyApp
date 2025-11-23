from ..crud import question_crud
from sqlmodel import Session
from ...models.question import QuestionCreate, Question
from sqlalchemy.exc import SQLAlchemyError
from ...core.exceptions import CouldNotCreateResource, NotFoundError, BaseException

import uuid 


def check_order_of_questions(questions: list[QuestionCreate]) -> bool:
    positions_list = tuple((question.position) for question in questions)
    is_ordered = len(questions) == len(positions_list)

    if is_ordered:
        return all(positions_list[i] + 1 == positions_list[i + 1] for i in range(len(positions_list) - 1))
    return False
    

def get_all_survey_questions(session: Session, survey_id: uuid.UUID) -> list[Question]:

    try:
        return question_crud.get_all_survey_questions(session=session, survey_id=survey_id)
    
    except SQLAlchemyError as e:
        raise BaseException(message="Database error")
    
    except Exception as e:
        raise BaseException(message="Could not find questions due to unexpected error")


def delete_survey_question(session: Session, question_id: uuid.UUID):

    question = question_crud.get_question_by_id(session=session, question_id=question_id)

    if question is None:
        raise NotFoundError(message="Could not find question with given id")

    question_crud.delete_question(session=session, question=question)
    

def delete_exsited(session: Session, survey_id = uuid.UUID): 
    questions = get_all_survey_questions(session=session, survey_id=survey_id)

    for question in questions:
        delete_survey_question(session=session, question_id=question.id)


def create_or_update_questions_for_survey(session: Session, questions: list[QuestionCreate], survey_id = uuid.UUID) -> list[Question]:

    is_ordered = check_order_of_questions(questions = questions)
    if not is_ordered:
        raise CouldNotCreateResource(message="The proper order of questions was not followed")

    created = []

    try:

        delete_exsited(session=session, survey_id=survey_id)

        for question_base in questions:
            q = question_crud.create_question(session=session, question_base=question_base, survey_id=survey_id)
            created.append(q)

        session.commit()

        for q in created:
            session.refresh(q)
        
        return created
    
    except SQLAlchemyError as e:
        session.rollback()
        raise CouldNotCreateResource(message="Database error while creating questions")
    
    except Exception as e:
        session.rollback()
        raise CouldNotCreateResource(message="Could not create questions due to unexpected error")