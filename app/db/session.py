from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)
Sessionlocal= sessionmaker[Session](bind=engine)


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()