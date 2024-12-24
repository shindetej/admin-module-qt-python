
import sys,random
from PySide6.QtCore import Qt,QTimer,Signal
from PySide6.QtGui import QColor

from PySide6.QtWidgets import QApplication,QWidget,QLabel, QDialog, QPushButton, QVBoxLayout, QLineEdit,QComboBox,QHBoxLayout,QMessageBox
import sys
import os.path
run_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(run_path)
sys.path.append(run_path)
from repository.masterdb import AdminDatabaseManager

from ui.custom_dialog import CustomDialog
from utilities import status_file


# -------- LOGGER ---------------
from logs import logs
import logging
global logger 
logger = logging.getLogger("frontend")
logger.setLevel(logging.DEBUG)
from datetime import date
today = date.today()
file_handler = logging.FileHandler(str(run_path) + "/logs/frontend-" + str(today) + ".log") #create filehandler
formatter = logging.Formatter('%(asctime)s %(message)s') #create formatter
file_handler.setFormatter(formatter) #add formatter to file_handler
logger.handlers=[file_handler]  #file handler replaced 
# -----------------------

class UserAddDialogBox(QDialog):
    add_new_user_signal = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add user form")


         # --- LOGGER ---    
        logs.logJson['ModuleName']="UserAddWidget"
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']
        logs.logJson['Tag']="UserAddWidget"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson) 
        # ---  ---  ----
        

        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('white'))
        self.setAutoFillBackground(True)
        self.setPalette(pal)

        self.setModal(True)  # Ensure modal behavior
        self.resize(400, 400)  # Set width and height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.admin_repo = AdminDatabaseManager()
        self.admin_repo.connect()
        
        # SAVE button enable flags initialize
        self.flag_validate_password  = False
        self.user_criteria_valid = False
        self.passwords_match = False

        self.form_layout = QVBoxLayout()

        self.add_user_label = QLabel("Add New User")
        self.add_user_label.setObjectName('label_useradd')
        self.add_user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_user_label.setStyleSheet('#label_useradd {font-family: Calibri;font-size: 16pt;font-weight: bold;color: #C2222E;}')
        self.add_user_label.setFixedHeight(42)

        self.form_layout.addWidget(self.add_user_label,alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.role_combo = QComboBox()
        self.role_combo.addItem("Select Role")
        self.roles_list =self.admin_repo.get_role_name_list()
        list_of_roles = [entry['roleName'] for entry in self.roles_list ]
        self.role_combo.addItems(list_of_roles)
        # self.role_combo.addItems(["Admin", "Operator", "Developer"])
        self.role_combo.setCurrentIndex(0)
        self.role_combo.setStyleSheet('''
                    QComboBox {
                        border:1px solid #C2222E;
                        height: 40px;
                    }
                    QComboBox::drop-down:button { image: url(assets/images/dropdown_Icon_small.png);background-color:white;}
                    
                    QComboBox::item {height:35px;border-bottom:1px solid black;background:white}
                    QComboBox::item:hover {
                        background-color: grey;
                    }
                    QComboBox::item:selected {
                        background-color: grey;
                        color: white;
                    }''')
        self.userlist = self.admin_repo.get_username_list()
        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter username")
        self.username.textChanged.connect(self.enable_submit_button)

        self.username.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.username.setFixedHeight(45)
        
        self.username_warning = QLabel()
        self.username_warning.hide() 
        self.username_warning.setStyleSheet("color: red;font-size: 9pt;font-family: calibri;font-style: italic;")



        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("Enter First Name")
        self.first_name.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.first_name.setFixedHeight(45)

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Enter Last Name")
        self.last_name.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.last_name.setFixedHeight(45)

        self.empid = QLineEdit()
        self.empid.setPlaceholderText("Enter Employee Id")
        self.empid.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.empid.setFixedHeight(45)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.textChanged.connect(self.enable_submit_button)
        self.password.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.password.setFixedHeight(45)

        self.validation_labels = {
            "length": QLabel("Use 8 or more characters"),
            "upper": QLabel("Use least one uppercase letter (e.g. AB)"),
            "lower": QLabel("Use least one lowercase letter (e.g. ab)"),
            "digit": QLabel("Use a number (e.g. 123)"),
            "symbol": QLabel("Use least one symbol (e.g. @#%)")
        }

    
        self.re_password = QLineEdit()
        self.re_password.setPlaceholderText("Re-Enter Password")
        self.re_password.setEchoMode(QLineEdit.Password)
        self.re_password.setStyleSheet("border: 1px solid #C2222E; font-size: 16px; padding-left:10px;")
        self.re_password.setFixedHeight(45)

        self.match_label = QLabel()
        self.match_label.setText("Password matched")
        self.match_label.setStyleSheet("color: green;")  
        self.match_label.hide()  

        self.re_password.textChanged.connect(self.enable_submit_button)
        

        buttons_widget =  QWidget()
        self.button_hbox =  QHBoxLayout(buttons_widget)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedHeight(40)
        self.btn_cancel.setStyleSheet("font-family: Calibri; font-size: 16px; font-weight: 600; color: #C2222E; background-color: #FFFFFF; border:1px solid #C2222E;")
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
       
        self.btn_save = QPushButton("Save")
        self.btn_save.setFixedHeight(40)
        self.btn_save.setStyleSheet("font-family: Calibri; font-size: 16px; font-weight: 600; color: #FFFFFF; background-color: #C2222E; border:1px solid #C2222E;")
        self.btn_save.setEnabled(False) 

        self.btn_save.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.reject)
        self.button_hbox.addWidget(self.btn_cancel)
        self.button_hbox.addWidget(self.btn_save)

        self.form_layout.addWidget(self.role_combo)
        self.form_layout.addWidget(self.username)
        self.form_layout.addWidget(self.username_warning)

        self.form_layout.addWidget(self.first_name)
        self.form_layout.addWidget(self.last_name)
        self.form_layout.addWidget(self.empid) 
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

    def check_username_validity(self):
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']="In check_username_validity"
        logger.info(logs.logJson) 
        uname = self.username.text()

        if len(uname) < 4:
            print("USERNAME SHOULD HAVE A MINIMUM OF 4 CHARACTERS.")
            self.username_warning.setText("Username should have a minimum of 4 characters.")
            self.user_criteria_valid = False
            self.username_warning.show() 
        elif uname in self.userlist:
            self.username_warning.setText("Username already exists in database.")
            self.username_warning.show() 
            self.user_criteria_valid = False
        else:
            self.username_warning.hide() 
            self.user_criteria_valid = True
        
        



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
            self.password_criteria.hide()
        else:
            label.show()
            self.password_criteria.show()

            

    def confirm_password(self):
        password_validated=  self.password.text()
        password_confirmed =  self.re_password.text()
 
        self.passwords_match = False
        if password_validated and password_confirmed  and password_validated == password_confirmed:  # Passwords match
                self.passwords_match = True


    def enable_submit_button(self):


        self.check_username_validity()

        if self.user_criteria_valid  :
            self.validate_password_format()
            if   self.flag_validate_password and self.passwords_match:
                print("IF FLAG_VALIDATE_PASSWORD  AND PASSWORDS_MATCH ")

                self.match_label.show()
                self.enable_save_button()
            else:
                self.match_label.hide()
                self.disable_save_button()
        else :
            print("\n-----\nUSERNAME INVALID CRITERIA")   
            self.disable_save_button() 


    def enable_save_button(self):
        self.btn_save.setEnabled(True)
        self.btn_save.setCursor(Qt.PointingHandCursor)

    def disable_save_button(self):
        self.btn_save.setEnabled(False)
        self.btn_save.setCursor(Qt.ArrowCursor)                          

    
    def submit_form(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']="In submit_form"
        logger.info(logs.logJson) 

        empid_flag = False
        fname_flag = False
        lname_flag = False
        role_selection_flag = False
        associated_role_id = None

        empid = self.empid.text()
        fname = self.first_name.text()
        lname = self.last_name.text()
        username = self.username.text()
        passwd = self.password.text()

        if self.empid.text():
            empid_flag = True
        else :
            self.pop_up_failure_message("Enter Employee Id")
            logs.logJson['Message']="In submit_form : Enter Employee Id"
            logger.info(logs.logJson)   


        if self.first_name.text():
            fname_flag = True
        else :
            self.pop_up_failure_message("Enter First Name")
            logs.logJson['Message']="In submit_form : Enter First Name"
            logger.info(logs.logJson)   


        if self.last_name.text():
            lname_flag = True
        else :
            self.pop_up_failure_message("Enter Last Name")
            logs.logJson['Message']="In submit_form : Enter Last Name"
            logger.info(logs.logJson)  
            
        role_selected = self.role_combo.currentText()
        # Check if the placeholder item is selected
        if role_selected == "Select Role":
            role_selection_flag = False 
            logger.info("Please select a class.")
            self.pop_up_failure_message("Select Role From List")
        else : 
            role_selection_flag =  True

        
        if empid_flag and fname_flag and lname_flag and role_selection_flag:
            # Search for the roleName in the list of dictionaries
            for entry in self.roles_list:
                if entry['roleName'] == role_selected:
                    associated_role_id = entry['roleId']
                    print(f"The role id associated with roleName '{role_selected}' is: {associated_role_id}")
                    break
            if associated_role_id :
                print("Before adding user")
                self.admin_repo.add_user(username,fname,lname,empid,passwd,associated_role_id)
                print("After adding user")
                self.add_new_user_signal.emit()
                self.pop_up_success_message("User Added Successfully")
                self.close()
            else:
                self.pop_up_failure_message("Failed To Add New User")
                self.close()

    
    
    def closeAfterTimeout(self):
        self.mb.close()
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.focusNextChild()




    def pop_up_success_message(self,message):
        self.mb =  CustomDialog(message,status_file.successStatusCode)
        self.mb.exec()
 

    def pop_up_failure_message(self,message):
        self.mb =  CustomDialog(message,status_file.errorMsg)
        self.mb.exec()

if __name__ == "__main__": 
    app =  QApplication(sys.argv)

    window =UserAddDialogBox()
    window.show()

    app.exec()