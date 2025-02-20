bl_info = {
    "name": "Transform Manager",
    "author": "Yogesh Sharma",
    "version": (1, 1),
    "blender": (4, 3, 2),
    "category": "Object",
    "description": "Manage object transforms and send data to a server"
}

import bpy
import sys
import os

# Ensure websockets is loaded from the local websockets_lib folder
websockets_path = os.path.join(os.path.dirname(__file__), "websockets_lib")
if websockets_path not in sys.path:
    sys.path.append(websockets_path)

# Import modules after modifying sys.path
import websockets
from .panels import panel_classes
from .operators import operator_classes
from .websocket_manager import WebSocketManager  # Import class instead of instance

# Define InventoryItem PropertyGroup
class InventoryItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Item Name", default="")
    quantity: bpy.props.IntProperty(name="Quantity", default=1)

def register():
    from bpy.props import (EnumProperty, PointerProperty, StringProperty, 
                           IntProperty, BoolProperty, CollectionProperty)

    # Register InventoryItem class first
    bpy.utils.register_class(InventoryItem)
    
    # Scene Properties
    bpy.types.Scene.inventory_loaded = BoolProperty(
        name="Inventory Loaded",
        default=False
    )
    
    bpy.types.Scene.selected_object = PointerProperty(
        type=bpy.types.Object,
        name="Selected Object"
    )
    
    bpy.types.Scene.cached_inventory = CollectionProperty(
        type=InventoryItem,
        name="Cached Inventory"
    )
    
    bpy.types.Scene.show_inventory = BoolProperty(
        name="Show Inventory",
        default=False
    )
    
    bpy.types.Scene.endpoint_options = EnumProperty(
        name="Endpoint",
        description="Select which transform data to send",
        items=[
            ('transform', "Transform", "Send all transform data"),
            ('translation', "Translation", "Send only position data"),
            ('rotation', "Rotation", "Send only rotation data"),
            ('scale', "Scale", "Send only scale data"),
        ],
        default='transform'
    )
    
    bpy.types.Scene.item_name = StringProperty(
        name="Item Name",
        default=""
    )
    
    bpy.types.Scene.item_quantity = IntProperty(
        name="Quantity",
        default=1
    )
    
    # Register all panel and operator classes
    for cls in panel_classes + operator_classes:
        bpy.utils.register_class(cls)
    
    # ✅ Start WebSocket Manager **after** all properties are registered
    global ws_manager
    ws_manager = WebSocketManager()
    ws_manager.start()

def unregister():
    # Unregister all panel and operator classes
    for cls in reversed(panel_classes + operator_classes):
        bpy.utils.unregister_class(cls)
    
    # Unregister InventoryItem class
    bpy.utils.unregister_class(InventoryItem)
    
    # Remove all properties
    del bpy.types.Scene.selected_object
    del bpy.types.Scene.endpoint_options
    del bpy.types.Scene.item_name
    del bpy.types.Scene.item_quantity
    del bpy.types.Scene.cached_inventory
    del bpy.types.Scene.inventory_loaded
    del bpy.types.Scene.show_inventory

if __name__ == "__main__":
    register()
