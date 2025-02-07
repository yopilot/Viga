# triggers.py
from sqlalchemy import event
from .models import InventoryItem
from fastapi import WebSocket
from typing import List
import asyncio

connected_clients: List[WebSocket] = []

async def broadcast_inventory_update(inventory_data):
    inventory_list = [{"name": item.name, "quantity": item.quantity} for item in inventory_data]
    for client in connected_clients:
        try:
            await client.send_json(inventory_list)
        except:
            connected_clients.remove(client)

@event.listens_for(InventoryItem, 'after_insert')
@event.listens_for(InventoryItem, 'after_update')
@event.listens_for(InventoryItem, 'after_delete')
def after_inventory_change(mapper, connection, target):
    from .crud import get_inventory
    from .base import SessionLocal
    
    db = SessionLocal()
    try:
        inventory = db.query(InventoryItem).all()
        asyncio.create_task(broadcast_inventory_update(inventory))
    finally:
        db.close()
