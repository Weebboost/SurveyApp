from fastapi import APIRouter, Depends
from ..models.submission import SubmissionCreate
from ..core.db import get_session
from sqlmodel import Session
from fastapi import APIRouter, Depends
from ..logic.service import submission_service

router = APIRouter (
    prefix = "/submissions",
    tags = ["submission"]
)

@router.post("/")
def submit_submission(*, session: Session = Depends(get_session), submission_create: SubmissionCreate):
    return submission_service.submit_submission(session = session, submission_create = submission_create)