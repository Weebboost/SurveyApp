from sqlmodel import create_engine, Session, SQLModel
from ..core.config import settings
from sqlalchemy.pool import StaticPool

engine = create_engine (
    settings.DATABASE_URL, 
    poolclass = StaticPool,
    echo=True
)

SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session