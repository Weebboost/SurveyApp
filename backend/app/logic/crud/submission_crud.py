from sqlmodel import Session, select
from ...models.submission import Submission
import uuid

def create_submission(session: Session, submission: Submission) -> Submission:
    session.add(submission)
    return submission