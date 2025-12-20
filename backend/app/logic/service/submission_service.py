from sqlmodel import Session
from ...models.submission import SubmissionCreate, Submission
from .answer_service import submit_answers
from ...core.transaction import transactional
from ..crud.submission_crud import create_submission
from ..service.question_service import get_questions_by_survey_id
from ...core.exceptions import CouldNotCreateResource

def validate_submission_creation(session: Session, submission_create: SubmissionCreate) -> None:

    questions = get_questions_by_survey_id(session = session, survey_id = submission_create.survey_id)
    question_ids = {question.id for question in questions}

    if len(submission_create.answers) != len(question_ids):
        raise CouldNotCreateResource("Number of answers does not match number of questions in the survey.")

    for answer in submission_create.answers:
        if answer.question_id not in question_ids:
            raise CouldNotCreateResource(f"Invalid question ID in answers: {answer.question_id}")
        

@transactional()
def submit_submission(*, session: Session, submission_create: SubmissionCreate):

    validate_submission_creation(session = session, submission_create = submission_create)

    answers = submission_create.answers

    submission = Submission.model_validate(
        submission_create.model_dump(exclude={"answers"})
    )
    print("Submission to create:", submission)
    created_submission = create_submission(session = session, submission = submission)

    submit_answers(
        session = session,
        answers_create = answers,
        submission_id = created_submission.id
    )
    