from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging
import asyncio
from api.endpoints import router
import uvicorn
from database.triggers import connected_clients, broadcast_inventory_update
from database.crud import get_inventory
from database.db import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="DCC Transform & Inventory API", version="1.0")
app.include_router(router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected")
    connected_clients.append(websocket)
    
    try:
        # Send initial inventory data
        db = next(get_db())
        inventory = get_inventory(db)
        await websocket.send_json(inventory)
        
        while True:
            # Keep connection alive and wait for any messages
            await websocket.receive_text()
            
    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
        connected_clients.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)

@app.middleware("http")
async def log_request(request, call_next):
    logger.info(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/")
def read_root():
    return {"message": "FastAPI Server Running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        reload=True,
        reload_delay=2  # Increase the delay between reloads to 2 seconds
    )
