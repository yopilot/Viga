# database/db.py
from .base import engine, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
