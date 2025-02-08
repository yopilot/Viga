# Viga Assignment

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

# ScreenShot

## plugin
![Screenshot 2025-02-09 025200](https://github.com/user-attachments/assets/f77c1077-cbec-4ae4-ad85-61f186c99f8d)
![Screenshot 2025-02-09 030615](https://github.com/user-attachments/assets/bab2257c-62c0-4ed3-91be-f21e29b59a19)

## Fast api run
![Screenshot 2025-02-09 025215](https://github.com/user-attachments/assets/de2bd944-34f3-47ca-a028-06e0b6714879)
## Data Storage at Server - SQLite


### Inventory Data
![Screenshot 2025-02-09 025238](https://github.com/user-attachments/assets/c14af6d5-303d-405b-b346-92afa5e7a8ae)

---

## Executable PYQt Application for Inventory

### Application
![Screenshot 2025-02-09 025355](https://github.com/user-attachments/assets/e6511e14-900a-4eef-8804-8f3c230d878e)

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

