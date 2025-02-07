from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path

# Correct path to models.py
MODELS_PATH = Path(r"C:\Users\Yaxh\Desktop\Viga\fastapi_server\database\models.py")
FASTAPI_SERVER_PATH = Path(r"C:\Users\Yaxh\Desktop\Viga\fastapi_server")

# Import models directly
import importlib.util
spec = importlib.util.spec_from_file_location("models", str(MODELS_PATH))
models = importlib.util.module_from_spec(spec)
spec.loader.exec_module(models)
InventoryItem = models.InventoryItem
Base = models.Base

class DatabaseManager:
    def __init__(self):
        # Using absolute path to your database file
        db_path = FASTAPI_SERVER_PATH / "inventory.db"
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