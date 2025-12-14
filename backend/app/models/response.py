import uuid

from sqlmodel import SQLModel, Field

class ResponseBase(SQLModel):
    survey_id: uuid.UUID
    question_id: uuid.UUID
    response: str


class ResponseCreate(ResponseBase):
    pass


class Response(ResponseBase, table = True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)