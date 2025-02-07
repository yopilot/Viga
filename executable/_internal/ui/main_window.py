from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon
from .inventory_widget import InventoryWidget  # Use relative import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Inventory Management System")
        self.setWindowIcon(QIcon('C:/Users/Yaxh/Desktop/Viga/PyQtApp/src/assets/logo.png'))  # Use forward slashes
        self.setMinimumSize(800, 600)

        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Apply modern dark theme to the main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1c1c1c;
            }
            QWidget#central_widget {
                background-color: #232323;
                border-radius: 10px;
            }
        """)

        # Add inventory widget
        self.inventory_widget = InventoryWidget()
        layout.addWidget(self.inventory_widget)
