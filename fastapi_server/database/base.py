import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Get the user's home directory
home_dir = os.path.expanduser("~")
# Specify the path for the SQLite database in the VigaData directory
db_dir = os.path.join(home_dir, "VigaData")
# Ensure the directory exists
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, "inventory.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()