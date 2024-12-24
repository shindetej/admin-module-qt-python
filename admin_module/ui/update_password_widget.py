
import sys,json
from PySide6.QtCore import Qt,Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication,QWidget,QLabel, QDialog, QPushButton, QVBoxLayout, QLineEdit,QComboBox,QHBoxLayout,QMessageBox
import sys
import os.path
run_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(run_path)
sys.path.append(run_path)
from repository.masterdb import AdminDatabaseManager
from ui.custom_dialog import CustomDialog
from utilities import status_file


class PasswordUpdateDialogBox(QDialog):
    after_password_updated = Signal()
    def __init__(self,username,parent=None):
        super().__init__(parent)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('white'))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.username = username
        self.current_password_verified = False
        self.setModal(True)  # Ensure modal behavior
        self.resize(400, 300)  # Set width and height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.admin_repo = AdminDatabaseManager()
        self.admin_repo.connect()
        
        # SAVE button enable flags initialize
        self.flag_validate_password  = False
        self.passwords_match = False

        self.form_layout = QVBoxLayout()
        self.update_pass_label = QLabel("Update Password")
        self.update_pass_label.setFixedSize(400, 30)
        self.update_pass_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.update_pass_label.setStyleSheet('font-family: Helvetica;font-size: 18pt;font-weight: bold;color: #C2222E;')

        self.form_layout.addWidget(self.update_pass_label)
        self.form_layout.addSpacing(15)

        
        self.password = QLineEdit()
        self.password.setFixedHeight(40)
        self.password.setPlaceholderText("Enter New Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.password.textChanged.connect(self.enable_submit_button)

        self.validation_labels = {
            "length": QLabel("Use 8 or more characters"),
            "upper": QLabel("Use least one uppercase letter (e.g. AB)"),
            "lower": QLabel("Use least one lowercase letter (e.g. ab)"),
            "digit": QLabel("Use a number (e.g. 123)"),
            "symbol": QLabel("Use least one symbol (e.g. @#%)")
        }

    
        self.re_password = QLineEdit()
        self.re_password.setFixedHeight(40)
        self.re_password.setPlaceholderText("Re-Enter New Password")
        self.re_password.setEchoMode(QLineEdit.Password)
        self.re_password.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.re_password.textChanged.connect(self.enable_submit_button)
        # ----------------------------------
        self.match_label = QLabel()
        self.match_label.setText("Password matched")
        self.match_label.setStyleSheet("color: green;")
        self.match_label.hide()

        buttons_widget =  QWidget()
        self.button_hbox =  QHBoxLayout(buttons_widget)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.setStyleSheet("font-family: Calibri; font-size: 16px; font-weight: 600; color: #C2222E; background-color: #FFFFFF; border:1px solid #C2222E;")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.update_btn = QPushButton("Update")
        self.update_btn.setFixedHeight(40)
        self.update_btn.setStyleSheet("font-family: Calibri; font-size: 16px; font-weight: 600; color: #FFFFFF; background-color: #C2222E; border:1px solid #C2222E;")
        self.update_btn.setEnabled(False) 

        self.update_btn.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.reject)
        self.button_hbox.addWidget(self.btn_cancel)
        self.button_hbox.addWidget(self.update_btn)

        self.form_layout.addWidget(self.password) 

        self.password_criteria = QLabel("Password must fulfil following criteria")
        self.password_criteria.setStyleSheet("font-size: 12px;")
        self.form_layout.addWidget(self.password_criteria)
        for label in self.validation_labels.values():
            label.setStyleSheet("color: #A6A6A6; font-size: 10px; padding-left:10px;")
            self.form_layout.addWidget(label)

        self.form_layout.addWidget(self.re_password)
        self.form_layout.addWidget(self.match_label)
        self.form_layout.addStretch(1)
        self.form_layout.addWidget(buttons_widget)

        self.setLayout(self.form_layout)

  
    def enable_password_entry(self):
        self.re_password.setEnabled(self.current_password_verified)  
        self.password.setEnabled(self.current_password_verified)  
        
        
    def validate_password_format(self):
        password = self.password.text()
        self.confirm_password()
        
        # Perform validation checks
        has_length = len(password) >= 8
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_symbol = any(not char.isalnum() for char in password)
        
         # Update labels based on validation
        self.update_label('length', has_length)
        self.update_label('upper', has_upper)
        self.update_label('lower', has_lower)
        self.update_label('digit', has_digit)
        self.update_label('symbol', has_symbol)
        
        # all true then return true flag
        self.flag_validate_password = all([has_length, has_upper, has_lower, has_digit, has_symbol]) 

        
        

    def update_label(self, label_key, condition):
        label = self.validation_labels[label_key]
        if condition:
            label.setStyleSheet("color: green; font-size: 10px; padding-left:10px;")
        else:
            label.setStyleSheet("color: #A6A6A6; font-size: 10px; padding-left:10px;")
        
        # Hide all labels if all conditions are met
        if all(label.styleSheet() == "color: green; font-size: 10px; padding-left:10px;" for label in self.validation_labels.values()):
            for label in self.validation_labels.values():
                label.hide()
        else:
            label.show()

   

    def confirm_password(self):
        password_validated=  self.password.text()
        password_confirmed =  self.re_password.text()
 
        self.passwords_match = False
        if password_validated and password_confirmed  and password_validated == password_confirmed:  # Passwords match
                self.passwords_match = True
        
  


    def enable_submit_button(self):
        self.validate_password_format()

        if self.passwords_match and self.flag_validate_password:
            self.match_label.show()
            self.update_btn.setEnabled(True)
            self.update_btn.setCursor(Qt.PointingHandCursor)
        else:
            self.match_label.hide()
            self.update_btn.setEnabled(False)
            self.update_btn.setCursor(Qt.ForbiddenCursor)



    
    def submit_form(self):
        passwd = self.password.text()
        repasswd = self.re_password.text()
        if passwd == repasswd :
            self.admin_repo.edit_password_of_user(self.username,passwd,"test_user")
            print("After adding user")
            self.pop_up_success_message("User Password Updated Successfully")
            self.after_password_updated.emit()
            self.close()
        else :
            self.pop_up_failure_message("User Password Failed")




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

    window =PasswordUpdateDialogBox('asharma')
    window.show()

    app.exec()