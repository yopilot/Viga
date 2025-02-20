from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .base import SQLALCHEMY_DATABASE_URL, Base, engine, SessionLocal

class InventoryItem(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    quantity = Column(Integer, default=0)

class TransformRecord(Base):
    __tablename__ = "transforms"
    id = Column(Integer, primary_key=True, index=True)
    object_name = Column(String, index=True)
    position_x = Column(Float)
    position_y = Column(Float)
    position_z = Column(Float)
    rotation_x = Column(Float)
    rotation_y = Column(Float)
    rotation_z = Column(Float)
    scale_x = Column(Float)
    scale_y = Column(Float)
    scale_z = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class FilePathRecord(Base):
    __tablename__ = "file_paths"
    id = Column(Integer, primary_key=True, index=True)
    object_name = Column(String, index=True)
    file_path = Column(String)
    project_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)