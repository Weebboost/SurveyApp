import uuid

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .question import Question


class SurveyBase(SQLModel):
    name: str = Field(max_length=255)


class SurveyCreate(SurveyBase):
    expires_delta: int | None #minutes


class Survey(SurveyBase, table = True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime
    expires_at: datetime
    last_updated: datetime
    status: str = Field(default="private")
    is_active: bool = Field(default=False)

    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: "User" | None = Relationship(back_populates="surveys") 

    questions: "Question" | None = Relationship(back_populates="survey")
    

class SurveyPublic(SurveyBase):
    created_at: datetime
    expires_at: datetime
    last_updated: datetime
    status: str
    is_active: bool