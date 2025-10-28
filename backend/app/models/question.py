import uuid

from sqlmodel import SQLModel, Field

class QuestionBase(SQLModel):
    content: str
    position: int
    survey_id: uuid.UUID
    answer_type: str

class Question(QuestionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
