import sys,json
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from PySide6.QtWidgets import QApplication,QWidget,QLabel, QDialog, QPushButton, QVBoxLayout, QLineEdit,QComboBox,QHBoxLayout,QMessageBox
import sys,random
import os.path

# goto main path  ../../../
run_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(run_path)
sys.path.append(run_path)

from repository.masterdb import TMSDbMgr
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
# file_handler = logging.FileHandler(str(Path(pathlog).parent) + "/logs/frontend.log") #create filehandler
formatter = logging.Formatter('%(asctime)s %(message)s') #create formatter
file_handler.setFormatter(formatter) #add formatter to file_handler
logger.handlers=[file_handler]  #file handler replaced 
# -----------------------


class ModelAddDialogBox(QDialog):
    after_added_model =Signal()
    def __init__(self,parent=None):
        super().__init__(parent)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('white'))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        # --- Logger ---
        logs.logJson['ModuleName']="ModelAddDialogBox"
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']
        logs.logJson['Tag']="ModelAddDialogBox()"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson) 
        # --- --- ---

        self.setModal(True)  
        self.resize(400, 200)  # Set width and height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.TMS_repo = TMSDbMgr()
        self.TMS_repo.connect()
        
        self.form_layout = QVBoxLayout()

        self.header_label = QLabel("Add New Model")
        self.header_label.setFixedSize(400, 30)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.header_label.setStyleSheet('font-family: Helvetica;font-size: 18pt;font-weight: bold;color: #C2222E;')


        self.new_model = QLineEdit()
        self.new_model.setPlaceholderText("Enter Model Name")
        self.new_model.setObjectName("editDialog")
        self.new_model.setStyleSheet("height: 40px; font-size: 16pt;")

        self.new_model.textChanged.connect(self.check_model_exists)

        self.username_warning = QLabel()
        # self.username_warning.setStyleSheet("color: red;font-family: calibri;font-style: italic;")
        self.username_warning.setObjectName("TMSWarningLabel")
        self.username_warning.hide()  

        buttons_widget =  QWidget()
        self.button_hbox =  QHBoxLayout(buttons_widget)
        self.save_btn = QPushButton("Save")
        self.save_btn.setFixedSize(150, 40)
        self.save_btn.setStyleSheet("font-family: Calibri; font-size: 21px;font-weight:bold; color: #FFFFFF; background-color: #C2222E;border:none")
        self.save_btn.setEnabled(False) 
        self.save_btn.clicked.connect(self.submit_form)

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_cancel.setFixedSize(150, 40)
        self.btn_cancel.setStyleSheet("font-family: Calibri; font-size: 21px;font-weight:bold; color: #C2222E; background-color: #FFFFFF;border:1px solid #C2222E")

        self.button_hbox.addWidget(self.btn_cancel)
        self.button_hbox.addWidget(self.save_btn)

        self.form_layout.addWidget(self.header_label)
        self.form_layout.addSpacing(15)

        self.form_layout.addWidget(self.new_model)
        self.form_layout.addStretch(1)

        self.form_layout.addWidget(self.username_warning)
        self.form_layout.addStretch(1)

        self.form_layout.addWidget(buttons_widget)

        self.setLayout(self.form_layout)

    def check_model_exists(self):
        self.model_name = self.new_model.text()
        model_list = self.TMS_repo.get_model_list(self.model_name)
        self.flag_new_model_used = False

        if len(self.model_name) < 4:
            self.username_warning.setText("Minimum 3 Characters.")
            self.username_warning.show() 
        elif  any(item['modelName'] == self.model_name for item in model_list):
            self.username_warning.setText("Model name already exists ")
            self.username_warning.show() 
        else:
            self.username_warning.hide() 
            self.flag_new_model_used = True
        self.enable_submit_button()

    def enable_submit_button(self):
        if self.flag_new_model_used:
            self.save_btn.setEnabled(True)
        else:
            self.save_btn.setEnabled(False)
 
    def submit_form(self):
        logs.logJson['ModuleName']="ModelAddDialog"
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']
        logs.logJson['Tag']="submit_form"
        logs.logJson['Endpoint']="ModelAddDialogBox"
        logger.info(logs.logJson) 
       
        if self.model_name is not None :
            is_updated = self.TMS_repo.add_model(self.model_name)
            if is_updated : 
                self.pop_up_success_message(f"Model {self.model_name} Saved Successfully")
                logger.info("successMessage: Model Entry Added Successfully")
                
            else :
                print("Failed To Save Model")
                self.pop_up_failure_message(f"Failed To Save Model")
                logger.info("failureMessage: Model Entry Added Failed")


            self.after_added_model.emit()
            self.close()

    
    
    # def closeAfterTimeout(self):
    #     self.mb.close()
            

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


# if __name__ == "__main__": 
#     app =  QApplication(sys.argv)

#     app.exec()