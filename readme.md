# Viga

## Overview
Viga is a comprehensive project that integrates a FastAPI server with a PyQt application and a Blender plugin. The project aims to manage inventory items and their transformations, providing a seamless interface between the server, desktop application, and Blender.

## Project Structure
- **fastapi_server**: Contains the FastAPI server code.
- **PyQtApp**: Contains the PyQt application code.
- **BlenderPlugin**: Contains the Blender plugin code.

## FastAPI Server
The FastAPI server provides endpoints for managing inventory items and their transformations.

### Key Files
- `main.py`: Initializes the FastAPI app and sets up WebSocket connections.
- `api/endpoints.py`: Defines the API endpoints for inventory and transformation management.
- `database/db_manager.py`: Manages database connections and operations.
- `database/crud.py`: Contains CRUD operations for the database.

### Running the Server
To run the FastAPI server, use the following command:
```sh
python main.py

