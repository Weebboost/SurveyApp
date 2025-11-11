from fastapi import FastAPI
from .routes import user_router, login, survey_router
from .core.db import engine
from . import models
from sqlmodel import SQLModel

app = FastAPI()

app.include_router(user_router.router)
app.include_router(login.router)
app.include_router(survey_router.router)

@app.get("/")
def root():
    return {"message": "Hello in Survey APP"}