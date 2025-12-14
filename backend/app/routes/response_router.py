from fastapi import APIRouter, Depends
from ..models.response import ResponseCreate
from ..core.db import get_session
from sqlmodel import Session
from fastapi import APIRouter, Depends
from ..logic.service import response_service

router = APIRouter (
    prefix = "/response",
    tags = ["response"]
)

@router.post()
def submit_answer(*, session: Session = Depends(get_session), response: ResponseCreate):
    return response_service.submit_response(session = session, response = response)