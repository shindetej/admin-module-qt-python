import sys,json
from PySide6.QtGui import QColor

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication,QWidget,QLabel, QDialog, QPushButton, QVBoxLayout, QLineEdit,QComboBox,QHBoxLayout,QMessageBox
import sys
import os.path

# goto main path  ../../../
run_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(run_path)
sys.path.append(run_path)

from repository.masterdb import AdminDatabaseManager
from ui.custom_dialog import CustomDialog
from utilities import status_file

class UsernameUpdateDialogBox(QDialog):
    after_username_updated = Signal()
    def __init__(self,username,emp_id ,parent=None):
        super().__init__(parent)

        self.username = username
        self.emp_id = emp_id
        self.setModal(True)  
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('white'))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.resize(400, 300)  # Set width and height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.admin_repo = AdminDatabaseManager()
        self.admin_repo.connect()
        
        self.form_layout = QVBoxLayout()


        self.current_username_label = QLabel("Existing Username")
        self.current_username_label.setObjectName("labelDialog")

        self.header_label = QLabel("Update Username")
        self.header_label.setFixedSize(400, 30)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.header_label.setStyleSheet('font-family: Helvetica;font-size: 18pt;font-weight: bold;color: #C2222E;')


        self.current_username = QLineEdit()
        self.current_username.setText(self.username) 
        self.current_username.setFixedHeight(50)
        self.current_username.setStyleSheet("padding-left: 10px;")
        # Set style sheet to gray out the non-editable QLineEdit
        self.current_username.setObjectName("editDialog")
        self.current_username.setDisabled(True)

        # ---- ----   ---  ----
        self.current_model_label = QLabel("New User Name")
        self.current_model_label.setObjectName("labelDialog")
        self.new_username = QLineEdit()
        self.new_username.setStyleSheet("padding-left: 10px;")
        self.new_username.setFixedHeight(50)
        self.new_username.setPlaceholderText("New username")
        self.new_username.setObjectName("editDialog")
        # self.new_username.setStyleSheet("font-size: 16pt;")

        self.new_username.textChanged.connect(self.check_username_exist)

        self.username_warning = QLabel()
        self.username_warning.setStyleSheet("color: grey; font-size: 12px;")
        self.username_warning.hide()  

        buttons_widget =  QWidget()
        self.button_hbox =  QHBoxLayout(buttons_widget)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.setStyleSheet("font-family: Calibri; font-size: 14px; font-weight: 600; color: #C2222E; background-color: #FFFFFF; border: 1px solid #C2222E;")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
       
        self.update_btn = QPushButton("Update")
        self.update_btn.setFixedHeight(40)
        self.update_btn.setStyleSheet("font-family: Calibri; font-size: 14px; font-weight: 600; color: #FFFFFF; background-color: #C2222E; border: 1px solid #C2222E;")

        self.update_btn.setEnabled(False) 

        self.update_btn.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.reject)
        self.button_hbox.addWidget(self.btn_cancel)
        self.button_hbox.addWidget(self.update_btn)

        self.form_layout.addWidget(self.header_label)
        self.form_layout.addSpacing(15)

        self.form_layout.addWidget(self.current_username_label)
        self.form_layout.addWidget(self.current_username)
        self.form_layout.addWidget(self.new_username)
        self.form_layout.addStretch(1)

        self.form_layout.addWidget(self.username_warning)
        self.form_layout.addStretch(1)

        self.form_layout.addWidget(buttons_widget)

        self.setLayout(self.form_layout)

    def check_username_exist(self):
        uname = self.new_username.text()
        oname = self.current_username.text()
        # userlist = self.admin_repo.get_username_list()
        self.flag_new_username_used = False

        if len(uname) < 4:
            self.username_warning.setText("Username should have a minimum of 4 characters.")
            self.username_warning.show() 
        elif uname == oname:
            self.username_warning.setText("Username is same as current username")
            self.username_warning.show() 
        # elif  userlist.count(uname) > 1:
        #     self.username_warning.setText("Username has multiple records with same username.")
        #     self.username_warning.show() 
        else:
            self.username_warning.hide() 
            self.flag_new_username_used = True
        self.enable_submit_button()

    def enable_submit_button(self):
        if self.flag_new_username_used:
            self.update_btn.setEnabled(True)
            self.update_btn.setCursor(Qt.PointingHandCursor)
        else:
            self.update_btn.setEnabled(False)
 
    def submit_form(self):
        nuname = self.new_username.text()
        if nuname :
            is_updated = self.admin_repo.edit_username_of_existing_user(self.emp_id,nuname,"test_user")
            if is_updated : 
                print("After updating username query")
                self.pop_up_success_message("User Username Updated Successfully")
            else :
                print("Failed Update username")
                self.pop_up_failure_message("User Username Update Failed")
            self.after_username_updated.emit()
            self.close()


            
    def pop_up_success_message(self,message):
        self.mb =  CustomDialog(message,status_file.successStatusCode)
        self.mb.exec()
 

    def pop_up_failure_message(self,message):
        self.mb =  CustomDialog(message,status_file.errorMsg)
        self.mb.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            focus_widget = QApplication.focusWidget()
            focus_widget.focusNextChild()
        else:
            super().keyPressEvent(event) 


if __name__ == "__main__": 
    app =  QApplication(sys.argv)

    window =UsernameUpdateDialogBox('asharma',1234)
    window.show()

    app.exec()