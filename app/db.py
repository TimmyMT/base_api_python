from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://postgres@localhost:5432/base_api_python"
# DATABASE_URL = "postgresql+psycopg2://postgres:postgres@fastapi_test_db:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
