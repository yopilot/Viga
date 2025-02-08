from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Import models directly
from . import models

InventoryItem = models.InventoryItem
Base = models.Base

class DatabaseManager:
    def __init__(self):
        # Get the user's home directory
        home_dir = os.path.expanduser("~")
        # Specify the path for the SQLite database in the VigaData directory
        db_dir = os.path.join(home_dir, "VigaData")
        # Ensure the directory exists
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "inventory.db")
        db_url = f"sqlite:///{db_path}"
        
        # Create engine with absolute path
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_all_items(self):
        session = self.SessionLocal()
        try:
            return session.query(InventoryItem).all()
        finally:
            session.close()

    def update_item_quantity(self, item_name, new_quantity):
        session = self.SessionLocal()
        try:
            item = session.query(InventoryItem).filter_by(name=item_name).first()
            if item:
                item.quantity = new_quantity
                session.commit()
                return True
            return False
        finally:
            session.close()