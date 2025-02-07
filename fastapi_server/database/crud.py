from sqlalchemy.orm import Session
from .models import InventoryItem, TransformRecord, FilePathRecord
from datetime import datetime

def get_inventory(db: Session):
    """
    Retrieve all inventory items from the database
    """
    return [{"name": item.name, "quantity": item.quantity} for item in db.query(InventoryItem).all()]

def add_item(db: Session, name: str, quantity: int):
    try:
        db_item = InventoryItem(name=name, quantity=quantity)
        db.add(db_item)
        db.commit()
        return True
    except Exception as e:
        print(f"Error adding item: {e}")
        db.rollback()
        return False


def remove_item(db: Session, name: str):
    try:
        item = db.query(InventoryItem).filter(InventoryItem.name == name).first()
        if item:
            db.delete(item)
            db.commit()
            return True
        return False
    except Exception as e:
        print(f"Error removing item: {e}")
        db.rollback()
        return False

def update_quantity(db: Session, name: str, quantity: int):
    try:
        item = db.query(InventoryItem).filter(InventoryItem.name == name).first()
        if item:
            item.quantity = quantity
            db.commit()
            return True
        return False
    except Exception as e:
        print(f"Error updating quantity: {e}")
        db.rollback()
        return False

def save_transform_data(db: Session, name: str, position: list, rotation: list, scale: list):
    try:
        transform = TransformRecord(
            object_name=name,
            position_x=position[0], position_y=position[1], position_z=position[2],
            rotation_x=rotation[0], rotation_y=rotation[1], rotation_z=rotation[2],
            scale_x=scale[0], scale_y=scale[1], scale_z=scale[2]
        )
        db.add(transform)
        db.commit()
        return True
    except Exception as e:
        print(f"Error saving transform data: {e}")
        db.rollback()
        return False

def save_file_path(db: Session, object_name: str, file_path: str, project_path: str):
    try:
        file_data = FilePathRecord(
            object_name=object_name,
            file_path=file_path,
            project_path=project_path
        )
        db.add(file_data)
        db.commit()
        return True
    except Exception as e:
        print(f"Error saving file path: {e}")
        db.rollback()
        return False
