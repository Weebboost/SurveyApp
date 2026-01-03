from sqlmodel import Session
from ...models.submission import SubmissionCreate, Submission
from .answer_service import submit_answers, validate_answers_creation
from ...core.transaction import transactional
from ..repositories import submission_repository
from ..services.question_service import get_questions_by_survey_id
import uuid
    
@transactional()
def submit_submission(*, session: Session, submission_create: SubmissionCreate):

    questions = get_questions_by_survey_id(session = session, survey_id = submission_create.survey_id)
    validate_answers_creation(
        answers_create = submission_create.answers,
        questions = questions
    )
    
    submission = Submission.model_validate(
        submission_create.model_dump(exclude={"answers"})
    )
    created_submission = submission_repository.create_submission(session = session, submission = submission)
    
    answers = submission_create.answers
    submit_answers(
        session = session,
        answers_create = answers,
        submission_id = created_submission.id
    )


@transactional()
def get_survey_submissions(*, session: Session, survey_id: uuid.UUID):
    return submission_repository.get_all_survey_submissions(session=session, survey_id=survey_id)