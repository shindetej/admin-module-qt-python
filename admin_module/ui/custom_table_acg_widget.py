from PySide6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.current_page =1
        # self.rows_per_page = 10
        # row_height = 50  # Adjust this value to your preferred row height
        self.setObjectName("customTableQss")
        self.horizontalHeader().setFixedHeight(60)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        # Set the width of the vertical scrollbar
        # self.verticalScrollBar().setStyleSheet("QScrollBar:vertical {background: #E5E4E2; width: 25px; border-radius: 3px; }")

        # Set the width of the horizontal scrollbar
        # self.horizontalScrollBar().setStyleSheet("QScrollBar:horizontal { background: #E5E4E2; width: 25px; border-radius: 3px;}")
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table_widget.horizontalHeader().setStyleSheet("background-color: ivory;")
        self.setAlternatingRowColors(True)
        self.horizontalHeader().setFixedHeight(60)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setAlternatingRowColors(True)
        self.init_ui()

    def init_ui(self):
    # Set column icons for sorting
        header = self.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.header_clicked)
        header.setSortIndicatorShown(True)
        header.setSortIndicator(0, Qt.AscendingOrder)

    def header_clicked(self, index):
        order = self.horizontalHeader().sortIndicatorOrder()
        self.sortByColumn(index, order)
        self.horizontalHeader().setSortIndicator(index, order)