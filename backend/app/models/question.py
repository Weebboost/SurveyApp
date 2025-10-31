import uuid

from sqlmodel import SQLModel, Field, Relationship

class QuestionBase(SQLModel):
    content: str
    position: int
    answer_type: str

class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    survey_id: uuid.UUID

    answer_options: list['QuestionAnswerOption'] = Relationship(back_populates="question")



class QuestionAnswerOptionBase(SQLModel):
    question_id: uuid.UUID
    position: int
    text: str


class QuestionAnswerOptionCreate(QuestionAnswerOptionBase):
    question_position: int


class QuestionAnswerOption(QuestionAnswerOptionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    question: Question = Relationship(back_populates="answer_options")