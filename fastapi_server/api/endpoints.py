from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database.db import get_db
import database.crud as crud
from database.crud import add_item, remove_item, update_quantity, save_transform_data, save_file_path as crud_save_file_path
from fastapi import WebSocket
from typing import List
# endpoints.py
from database.triggers import connected_clients
import json

connected_clients: List[WebSocket] = []

class TransformData(BaseModel):
    name: str
    position: List[float]  # matches Blender's data
    rotation: List[float]
    scale: List[float]

class InventoryItem(BaseModel):
    name: str
    quantity: int

class ItemName(BaseModel):
    name: str

class TranslationData(BaseModel):
    name: str
    position: List[float]  # changed from location to position

class RotationData(BaseModel):
    name: str
    rotation: List[float]

class ScaleData(BaseModel):
    name: str
    scale: List[float]


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        connected_clients.remove(websocket)

async def broadcast_inventory_update(inventory):
    message = json.dumps({"type": "inventory_update", "inventory": inventory})
    for client in connected_clients:
        await client.send_text(message)

# Modify your existing inventory-related endpoints
# Modify your existing inventory-related endpoints
@router.post("/add-item")
async def add_item_endpoint(item: InventoryItem, db: Session = Depends(get_db)):
    if add_item(db, item.name, item.quantity):
        return {"message": f"Item {item.name} added successfully"}
    raise HTTPException(status_code=400, detail="Failed to add item")


@router.get("/inventory")
async def get_inventory(db: Session = Depends(get_db)):
    try:
        inventory_items = crud.get_inventory(db)
        return inventory_items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/transform")
async def receive_transform(data: TransformData, db: Session = Depends(get_db)):
    save_transform_data(db, data.name, data.position, data.rotation, data.scale)
    return {"message": "Transform data received and saved", "data": data.model_dump()}

@router.get("/file-path")
async def get_file_path(projectpath: bool = False):
    # For backward compatibility with existing GET requests
    return {"path": "C:/example_project/" if projectpath else "C:/example_project/file.blend"}

@router.post("/file-path")
async def save_file_path_endpoint(data: dict, db: Session = Depends(get_db)):
    if crud_save_file_path(db, "blender_file", data.get("file_path"), data.get("project_path")):
        return {"message": "File path saved successfully", 
                "file_path": data.get("file_path"),
                "project_path": data.get("project_path")}
    raise HTTPException(status_code=400, detail="Failed to save file path")



@router.post("/translation")
async def receive_translation(data: TranslationData, db: Session = Depends(get_db)):
    try:
        if crud.save_transform_data(db, data.name, data.position, [0,0,0], [1,1,1]):
            return {"message": "Translation data received", "position": data.position}
        raise HTTPException(status_code=400, detail="Failed to save translation data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/rotation")
async def receive_rotation(data: RotationData, db: Session = Depends(get_db)):
    try:
        # Convert rotation to rotation for database storage
        rotation = data.rotation
        if crud.save_transform_data(db, data.name, [0,0,0], rotation, [1,1,1]):  # Only storing rotation
            return {"message": "Rotation data received", "rotation": data.rotation}
        raise HTTPException(status_code=400, detail="Failed to save rotation data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/scale")
async def receive_scale(data: ScaleData, db: Session = Depends(get_db)):
    try:
        # Convert scale to scale for database storage
        scale = data.scale
        if crud.save_transform_data(db, data.name, [0,0,0], [0,0,0], scale):  # Only storing scale
            return {"message": "Scale data received", "scale": data.scale}
        raise HTTPException(status_code=400, detail="Failed to save scale data")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/add-item")
async def add_item_endpoint(item: InventoryItem, db: Session = Depends(get_db)):
    if add_item(db, item.name, item.quantity):  # Use imported function directly
        return {"message": f"Item {item.name} added successfully"}
    raise HTTPException(status_code=400, detail="Failed to add item")

@router.post("/remove-item")
async def remove_item_endpoint(item: ItemName, db: Session = Depends(get_db)):
    if crud.remove_item(db, item.name):
        return {"message": f"Item {item.name} removed successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/update-quantity")
async def update_quantity_endpoint(item: InventoryItem, db: Session = Depends(get_db)):
    if crud.update_quantity(db, item.name, item.quantity):
        return {"message": f"Item {item.name} quantity updated successfully"}
    raise HTTPException(status_code=400, detail="Failed to update quantity")

