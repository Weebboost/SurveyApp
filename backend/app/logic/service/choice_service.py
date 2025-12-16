from ...models.choice import Choice, ChoiceCreate
from ..crud.choice_crud import create_choice
from sqlmodel import Session

import uuid

def create_choices(session: Session, choices_create: list[ChoiceCreate], question_id: uuid.UUID):
    choices = []
    for choice_create in choices_create:
        choice = Choice.model_validate(choice_create, update = { "question_id" : question_id })
        choices.append(create_choice(session = session, choice = choice))

    return choices