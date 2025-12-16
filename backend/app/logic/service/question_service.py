from ..crud import question_crud
from sqlmodel import Session
from ...models.question import QuestionCreate, Question
from ...models.survey import Survey
from ...logic.service.survey_service import update_survey_last_updated
from ...core.exceptions import CouldNotCreateResource, NotFoundError
from ...core.transaction import transactional
from ..service.choice_service import create_choices
import uuid 


def is_correct_order(elements) -> bool:
    positions = tuple((obj.position) for obj in elements)

    if len(elements) == len(positions):
        return all(positions[i] + 1 == positions[i + 1] for i in range(len(positions) - 1)) and positions[0] == 0
    return False
    

@transactional()
def get_all_survey_questions(session: Session, survey_id: uuid.UUID) -> list[Question]:
    return question_crud.get_all_survey_questions(session=session, survey_id=survey_id)
    
    
@transactional()
def delete_survey_question(session: Session, question_id: uuid.UUID):

    question = question_crud.get_question_by_id(session=session, question_id=question_id)

    if question is None:
        raise NotFoundError(message="Could not find question with given id")

    question_crud.delete_question(session=session, question=question)
    

@transactional()
def delete_exsited(session: Session, survey_id = uuid.UUID): 
    questions = get_all_survey_questions(session=session, survey_id=survey_id)

    for question in questions:
        delete_survey_question(session=session, question_id=question.id)


def validate_questions_creation(questions: list[QuestionCreate], survey: Survey) -> None:

    if survey.status != "private":
        raise CouldNotCreateResource(message="Cannot modify questions of a survey that is not private")
    
    if not is_correct_order(elements=questions):
        raise CouldNotCreateResource(message="The proper order of questions was not followed")
        
    for question_base in questions:

        if question_base.choices and not is_correct_order(elements=question_base.choices):
            raise CouldNotCreateResource(message="The proper order of choices was not followed")
        
        if question_base.answer_type in ["close", "multiple"]:
            if not question_base.choices or len(question_base.choices) < 2:
                raise CouldNotCreateResource(message="Questions with close or multiple answer types must have at least two choices")
            
        if question_base.answer_type == "open":
            if question_base.choices:
                raise CouldNotCreateResource(message="Questions with open answer type cannot have choices")
    

@transactional(refresh_returned_instance=True)
def create_or_update_questions_for_survey(session: Session, questions: list[QuestionCreate], survey: Survey) -> list[Question]:

    validate_questions_creation(questions=questions, survey=survey)

    created = []
    delete_exsited(session=session, survey_id=survey.id)

    for question_base in questions:
        
        question_dict = question_base.model_dump(exclude="choices")

        question = Question.model_validate(question_dict, update={"survey_id": survey.id})
        new_question = question_crud.create_question(session=session, question=question)
        created.append(new_question)
        
        if question_base.choices:
            create_choices(session=session, choices_create=question_base.choices, question_id=new_question.id)

    update_survey_last_updated(session=session, survey_id=survey.id)

    return created
