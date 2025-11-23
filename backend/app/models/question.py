import uuid
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .survey import Survey
    from .choice import Choice


class Answer_type(str, Enum):
    open = "open"
    close = "close"
    multiple = "multiple"
    

class QuestionBase(SQLModel):
    content: str
    position: int
    answer_type: Answer_type


class QuestionCreate(QuestionBase):
    pass


class QuestionPublic(QuestionBase):
    pass


class Question(QuestionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    survey_id: uuid.UUID = Field(foreign_key="survey.id")

    choices: List["Choice"] = Relationship(back_populates="question")
    survey: "Survey" = Relationship(back_populates="questions")