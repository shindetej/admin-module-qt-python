
from PySide6.QtWidgets import  QPushButton, QDialog, QLabel, QVBoxLayout,QApplication,QFrame,QSpacerItem,QSizePolicy
from PySide6.QtCore import Qt,QTimer
from PySide6.QtGui import QPixmap,QFontDatabase,QFont
import sys,os
run_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CustomDialog(QDialog):
    def __init__(self,msg,status):
        super().__init__()

        self.setStyleSheet("background-color:white")
        self.setFixedSize(418,276)
        self.setWindowTitle("Custom Message Box")
        self.setWindowFlag(Qt.FramelessWindowHint) 

        
        # Create a label for the image
        image_label = QLabel()

        if status==200:
            image = QPixmap(run_path+"/assets/images/success.png") 
        else:
            image = QPixmap(run_path+"/assets/images/error.png")
        image_label.setPixmap(image)
        

        # Create a success/error label
        if status==200:
            main_label=QLabel("Successful")
        else:
            main_label=QLabel("Error")
        main_label.setStyleSheet("font-weight:500;font-size:24px;")


        # Create a message label
        message_label = QLabel(msg)
        message_label.setStyleSheet("font-weight:400;font-size:16px;color:#64748B;")
        # message_label.setPlainText("This is a custom message box with an image.\n\nYour message goes here.")

        #create horizontal line
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)  # Set the frame shape to a horizontal line
        horizontal_line.setStyleSheet("QFrame { border: 2px solid #E9E9E9; }")
        horizontal_line.setFrameShadow(QFrame.Sunken) 

        #create okay button
        okay_button = QPushButton("Okay")
        okay_button.setFixedSize(370,44)
        # okay_button.setStyleSheet("background-color:#1E3A8A;font-weight:500;color:#FFFFFF;border:none;font-size:16px;border-radius:5px")
        okay_button.setStyleSheet("font-family: Calibri; font-size: 14px; font-weight: 600; color: #FFFFFF; background-color: #C2222E;")
        okay_button.setCursor(Qt.PointingHandCursor)
        okay_button.clicked.connect(self.close)

        # Create a layout for the custom dialog
        layout = QVBoxLayout()
        layout.addItem(QSpacerItem(200,20,QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(image_label, alignment=Qt.AlignCenter)
        layout.addWidget(main_label, alignment=Qt.AlignCenter)
        layout.addWidget(message_label, alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(200,10,QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(horizontal_line)
        layout.addItem(QSpacerItem(200,10,QSizePolicy.Expanding, QSizePolicy.Minimum))
        layout.addWidget(okay_button,alignment=Qt.AlignCenter)
        layout.addItem(QSpacerItem(200,10,QSizePolicy.Expanding, QSizePolicy.Minimum))
        # Set the layout for the custom dialog
        self.setLayout(layout)
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.closeAfterTimeout)
        self.timer.start(2000)  # Auto close after 1 second
    
    def closeAfterTimeout(self):
        self.close()
# if __name__ == "__main__":
#     app =QApplication(sys.argv)
#     sub_window = CustomDialog("success/error",0)
#     sub_window.show()
#     sys.exit(app.exec())