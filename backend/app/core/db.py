from sqlmodel import create_engine, Session, SQLModel
from ..core.config import settings
from sqlalchemy.pool import StaticPool
from .. import models

engine = create_engine (
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass = StaticPool,
    echo=True
)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session