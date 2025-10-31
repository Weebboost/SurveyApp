import uuid

from sqlmodel import SQLModel, Field

class Response(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    survey_id: uuid.UUID
    question_id: uuid.UUID
    response: str