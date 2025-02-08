![logo](https://github.com/user-attachments/assets/240ce7d8-dcc8-45ac-a352-6f7ff69f3a82)
# Viga

## Overview
Viga is a comprehensive project that integrates a FastAPI server with a PyQt application and a Blender plugin. The project aims to manage inventory items and their transformations, providing a seamless interface between the server, desktop application, and Blender.

## Project Structure
- **fastapi_server**: Contains the FastAPI server code.
- **PyQtApp**: Contains the PyQt application code.
- **BlenderPlugin**: Contains the Blender plugin code.
- **VigaExecutable**: Contains the executable for the PyQt application.

## Full Setup Instructions

### Prerequisites
1. Install the Blender plugin:
    - Open Blender.
    - Go to `Edit` > `Preferences` > `Add-ons`.
    - Click `Install...` and select the `BlenderPlugin/transformPlugin.zip` file.
    - Enable the installed plugin.

2. Install the required Python packages:
    ```sh
    pip install -r fastapi_server/requirements.txt
    ```

### Running the Components
1. Navigate to the `fastapi_server` directory and run the FastAPI server:
    ```sh
    cd fastapi_server
    python main.py
    ```

2. Run the PyQt application:
    ```sh
    VigaExecutable/Viga/Vega.exe
    ```

## Additional Information

### FastAPI Server Endpoints
- **/transform**: Takes all transforms (position, rotation, scale).
- **/translation**: Takes only position.
- **/rotation**: Takes only rotation.
- **/scale**: Takes only scale.
- **/file-path**: Returns the DCC file's path. `/file-path?projectpath=true` returns the project folder path.
- **/add-item**: Adds an item to the database (name, quantity).
- **/remove-item**: Removes an item from the database (by name).
- **/update-quantity**: Updates an item's quantity (name, new quantity).

### Database
- Uses SQLite to store inventory items and quantities.
- The server updates the database based on `/add-item`, `/remove-item`, and `/update-quantity` requests.

### PyQt Application
- Displays the inventory from the database.
- Includes buttons to buy/return items, updating both the database and the DCC plugin's display.
- Ensures responsiveness while waiting for server responses.

### Bonus Features
- Single-binary packaging using PyInstaller.
- Advanced UI features.

## Requirements
- Knowledge of DCC Python API (Maya or Blender).
- REST API experience (Flask or FastAPI).
- SQLite database skills.
- Git for version control.

