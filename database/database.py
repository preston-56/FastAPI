from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
"""
The engine manages the connection to the database and handles query execution.
"""
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()