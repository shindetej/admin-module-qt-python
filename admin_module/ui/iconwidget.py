from PySide6.QtWidgets import QWidget,QHBoxLayout,QLabel
from PySide6.QtGui import QIcon, QColor, QPainter
from PySide6.QtCore import Qt
import os,sys
run_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class IconWidget(QWidget):
    def __init__(self,color=None) :
        super().__init__()
        if  color:
            self.bg_color = color
        else :
            self.bg_color = "white"
        
        self.icon_layout=QHBoxLayout(self)
        edit_icon=QIcon(run_path+"/assets/images/edit.png")
        delete_icon=QIcon(run_path+"/assets/images/delete.png")
        
        self.edit_label = QLabel()
        self.edit_label.setCursor(Qt.PointingHandCursor)
        self.delete_label = QLabel()
        self.delete_label.setCursor(Qt.PointingHandCursor)
        self.edit_label.setPixmap(edit_icon.pixmap(25, 25)) 
        self.delete_label.setPixmap(delete_icon.pixmap(25, 25)) 
        
        self.icon_layout.addWidget(self.edit_label)

        self.icon_layout.addSpacing(10)#add spacing

        self.icon_layout.addWidget(self.delete_label)

        self.icon_layout.setAlignment(Qt.AlignCenter)#align to center
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.bg_color)