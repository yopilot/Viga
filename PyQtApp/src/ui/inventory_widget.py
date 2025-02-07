from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QLabel, QHeaderView, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QIcon, QColor, QFont, QPixmap
from database.db_manager import DatabaseManager

class InventoryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.setup_ui()
        self.load_inventory()

    def setup_ui(self):
        self.setWindowIcon(QIcon('C:/Users/Yaxh/Desktop/Viga/PyQtApp/src/assets/logo.png'))
        self.setWindowTitle("Inventory Manager")
        self.setStyleSheet("background-color: #1E1E1E; color: #FFFFFF;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Centered logo with inversion effect
        self.logo_label = QLabel(self)
        pixmap = QPixmap('C:/Users/Yaxh/Desktop/Viga/PyQtApp/src/assets/logo.png').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        image = pixmap.toImage()
        image.invertPixels()
        inverted_pixmap = QPixmap.fromImage(image)
        self.logo_label.setPixmap(inverted_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("background-color: transparent;")
        layout.addWidget(self.logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Inventory Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #252525;
                color: #FFFFFF;
                border-radius: 10px;
                font-size: 15px;
            }
            QHeaderView::section {
                background-color: #1E1E1E;
                font-weight: bold;
                padding: 10px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #444;
            }
        """)
        
        table_shadow = QGraphicsDropShadowEffect()
        table_shadow.setBlurRadius(15)
        table_shadow.setColor(QColor(0, 0, 0, 100))
        table_shadow.setOffset(3, 3)
        self.table.setGraphicsEffect(table_shadow)

        layout.addWidget(self.table)

        # Button Layout
        button_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90E2;
                color: white;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6CA6E8;
            }
        """)
        self.refresh_btn.clicked.connect(self.load_inventory)
        button_layout.addWidget(self.refresh_btn)
        layout.addLayout(button_layout)

    def load_inventory(self):
        self.table.setRowCount(0)
        items = self.db_manager.get_all_items()

        for item in items:
            row = self.table.rowCount()
            self.table.insertRow(row)

            name_item = QTableWidgetItem(item.name)
            name_item.setForeground(QColor("#FFFFFF"))
            self.table.setItem(row, 0, name_item)

            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setForeground(QColor("#CCCCCC"))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, qty_item)

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            buy_btn = QPushButton("Buy")
            buy_btn.setStyleSheet("background-color: #27AE60; color: white; padding: 6px 12px;")
            return_btn = QPushButton("Return")
            return_btn.setStyleSheet("background-color: #E74C3C; color: white; padding: 6px 12px;")
            buy_btn.clicked.connect(lambda _, r=row: self.update_item(r, -1))
            return_btn.clicked.connect(lambda _, r=row: self.update_item(r, 1))
            actions_layout.addWidget(buy_btn)
            actions_layout.addWidget(return_btn)
            self.table.setCellWidget(row, 2, actions_widget)
        
    def update_item(self, row, quantity_change):
        item_name = self.table.item(row, 0).text()
        current_quantity = int(self.table.item(row, 1).text())
        new_quantity = current_quantity + quantity_change

        if new_quantity >= 0 and self.db_manager.update_item_quantity(item_name, new_quantity):
            self.table.item(row, 1).setText(str(new_quantity))
