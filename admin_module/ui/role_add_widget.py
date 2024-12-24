import sys,json
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication,QWidget,QLabel, QDialog, QPushButton, QVBoxLayout, QLineEdit,QComboBox,QHBoxLayout,QMessageBox
import sys,random
import os.path
from PySide6.QtGui import QColor


# goto main path  ../../../
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



class RoleAddWidget(QDialog):
    after_adding_new_role=Signal()
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setModal(True)  
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('white'))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.resize(300, 200)  # Set width and height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.TMS_repo = AdminDatabaseManager()
        self.TMS_repo.connect()

        # --- LOGGER ---    
        logs.logJson['ModuleName']="RoleAddWidget"
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']
        logs.logJson['Tag']="RoleAddWidget"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson) 
        # ---  ---  ----
        self.pre_loaded_role_list = json.loads(self.TMS_repo.get_role_details())
        # print(f"{self.pre_loaded_role_list}")
        # print(f"{self.pre_loaded_role_list['data']}")
        
        self.form_layout = QVBoxLayout()
        style_label = """
                            QLineEdit{
                        border:1px solid #C2222E;
                        height: 40px;
                        width:300px;
                        padding-left: 5px
                     }
                            """
        style_textbox = """
                     #editDialog
                        {
                            font-size: 11pt; 
                            max-width: 250px; 
                            height: 25px; 
                            color: #36454F;
                        }  
                        """
        self.setStyleSheet(style_label)
        # self.setStyleSheet(style_textbox)


        self.header_label = QLabel("Add New Role")
        self.header_label.setFixedSize(300, 30) 
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.header_label.setStyleSheet('font-family: Helvetica;font-size: 18pt;font-weight: bold;color: #C2222E;')
        self.form_layout.addWidget(self.header_label,Qt.AlignmentFlag.AlignHCenter)
        self.form_layout.addSpacing(10)

      

        
        self.form_part1 = QWidget()
        self.form_box_layout = QVBoxLayout(self.form_part1)
        self.form_box_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # -----------------Defect Type----------------
        self.role_name_label = QLabel("Role Name")
        self.role_name_label.setObjectName("labelDialog")
        self.form_box_layout.addWidget(self.role_name_label)
        
        
        self.role_name_edit = QLineEdit()
        self.role_name_edit.setObjectName("editDialog")
        self.role_name_edit.textChanged.connect(self.check_role_name_exist)
        self.form_box_layout.addWidget(self.role_name_edit)
        # self.form_box_layout.addStretch()

        self.role_name_warning = QLabel()
        self.role_name_warning.setStyleSheet("font-size: 10pt;color: red;font-family: calibri;font-style: italic;")
        self.role_name_warning.hide() 
        self.form_box_layout.addWidget(self.role_name_warning)
        self.form_box_layout.addSpacing(10)
        # -----------------Inspection Criteria----------------
        
        self.role_description_label = QLabel("Role Description")
        self.role_description_label.setObjectName("labelDialog")
        self.form_box_layout.addWidget(self.role_description_label)

        self.role_description_edit = QLineEdit()
        self.role_description_edit.setObjectName("editDialog")
        self.form_box_layout.addWidget(self.role_description_edit,Qt.AlignmentFlag.AlignCenter)
        self.form_layout.addWidget(self.form_part1,Qt.AlignmentFlag.AlignHCenter)

        self.form_box_layout.addSpacing(10)
        # -----------------Category no----------------

       

        buttons_widget =  QWidget()
        self.button_hbox =  QHBoxLayout(buttons_widget)
        # self.btn_cancel = QPushButton("Cancel")
        # self.save_btn = QPushButton("Save")
        self.btn_cancel = QPushButton("Cancel")
        self.save_btn = QPushButton("Save")
        self.save_btn.setEnabled(False) 
        self.save_btn.clicked.connect(self.submit_form)
        self.btn_cancel.clicked.connect(self.reject)
        self.save_btn.setStyleSheet("font-family: Calibri; font-size: 21px;font-weight:bold; color: #FFFFFF; background-color: #C2222E;border:none")
        self.btn_cancel.setStyleSheet("font-family: Calibri; font-size: 21px;font-weight:bold; color: #C2222E; background-color: #FFFFFF;border:1px solid #C2222E")
        self.save_btn.setFixedHeight(40)
        self.btn_cancel.setFixedHeight(40)
        self.button_hbox.addWidget(self.btn_cancel)
        self.button_hbox.addWidget(self.save_btn)


        self.form_layout.addStretch(0)


        self.form_layout.addWidget(buttons_widget)
        self.setLayout(self.form_layout)


    def check_role_name_exist(self):

        self.role_name = self.role_name_edit.text()
        self.flag_new_role_name = False

        if len(self.role_name) < 4:
            self.role_name_warning.setText("Minimum 3 Characters.")
            self.role_name_warning.show() 
        elif  any(item['roleName'] == self.role_name for item in self.pre_loaded_role_list['data']):
            self.role_name_warning.setText("Role already exists ")
            self.role_name_warning.show() 
        else:
            self.role_name_warning.hide() 
            self.flag_new_role_name = True
        self.enable_submit_button()

    def enable_submit_button(self):
        if self.flag_new_role_name:
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)
 
     
    def submit_form(self):
          # defect_id = self.defect_detail_by_id[0]['defectId']
        logs.logJson['ModuleName']="DefectWidget"
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']
        logs.logJson['Tag']="submit_form"
        logs.logJson['Endpoint']="defectTableWidget"
        logger.info(logs.logJson) 

        self.session_user = "test_dev_user"
        role_name = self.role_name_edit.text().title()
       
        role_desc = self.role_description_edit.text()
        

    
        is_updated = self.TMS_repo.add_new_role(role_name=role_name,role_description=role_desc,created_by=self.session_user)
        if is_updated : 
            print("New Role Added Successfully")
            self.pop_up_success_message("New Role Added Successfully")
            logger.info("successMessage: New Role Added Successfully")
        else :
            print("Defect entry Update Failed")
            self.pop_up_failure_message("New Role Entry Failed")
            logger.info("failureMessage: New Role Entry Failed")

        self.after_adding_new_role.emit()
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

    # APP
    # window = ButtonDemo()
    window = RoleAddWidget()
  

    window.show()
    app.exec()