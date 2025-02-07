# websocket_manager.py
import asyncio
import websockets
import json
import threading
import bpy

class WebSocketManager:
    def __init__(self):
        self.websocket = None
        self.is_connected = False
        self.inventory_data = {}
        self.ws_url = "ws://127.0.0.1:5000/ws"
        self.update_interval = 1.0  # Update every second
        
    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.ws_url)
            self.is_connected = True
            print("WebSocket connected successfully")
            await self.listen()
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            self.is_connected = False
            
    async def listen(self):
        while self.is_connected:
            try:
                message = await self.websocket.recv()
                inventory_data = json.loads(message)
                
                # Update the cached inventory
                bpy.types.Scene.cached_inventory = inventory_data
                
                # Reset inventory_loaded to force refresh
                bpy.context.scene.inventory_loaded = False
                
                # Force UI update
                self.update_ui()
                
            except Exception as e:
                print(f"WebSocket error: {e}")
                self.is_connected = False
                break

    def update_ui(self):
        # Force Blender to refresh the UI
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()
                
    def start(self):
        thread = threading.Thread(target=lambda: asyncio.run(self.connect()))
        thread.daemon = True
        thread.start()

ws_manager = WebSocketManager()
