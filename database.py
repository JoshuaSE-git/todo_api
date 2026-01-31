from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite+pysqlite:///memory:")


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
