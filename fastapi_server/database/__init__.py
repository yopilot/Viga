# database/__init__.py
from .base import Base, engine
from .models import InventoryItem, TransformRecord, FilePathRecord

# Create tables
Base.metadata.create_all(bind=engine)
