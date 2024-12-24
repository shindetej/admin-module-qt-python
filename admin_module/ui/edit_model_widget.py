import sys,json
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from PySide6.QtWidgets import QApplication,QWidget,QLabel, QDialog, QPushButton, QVBoxLayout, QLineEdit,QComboBox,QHBoxLayout,QMessageBox
import sys
import os.path

# goto main path  ../../../
run_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(run_path)
sys.path.append(run_path)

from repository.masterdb import TMSDatabaseManager
# project class imports
from utilities import status_file
from ui.custom_dialog import CustomDialog


class ModelUpdateDialogBox(QDialog):
    after_model_edited = Signal()
    def __init__(self,modelname,model_id,session_user,parent=None):
        super().__init__(parent)
        pal = self.palette()
        pal.setColor(self.backgroundRole(), QColor('white'))
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        self.modelname = modelname
        self.model_id = model_id
        self.session_user = session_user
        self.setModal(True)  
        self.resize(400, 300)  # Set width and height
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.TMS_repo = TMSDatabaseManager()
        self.TMS_repo.connect()
        self.setStyleSheet("""
                            QLineEdit{
                        border:1px solid #C2222E;
                        height: 40px;
                        width:300px;
                        padding-left: 5px
                     }
                            """)
        self.form_layout = QVBoxLayout()

        self.header_label = QLabel("Update Model")
        self.header_label.setFixedSize(400, 30)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.header_label.setStyleSheet('font-family: Helvetica;font-size: 18pt;font-weight: bold;color: #C2222E;')


       
        self.current_model_label = QLabel("Existing Model Name")
        self.current_model_label.setObjectName("labelDialog")


        self.current_modelname = QLineEdit()
        self.setObjectName("editDialog")
        self.current_modelname.setText(self.modelname) 
        # Set style sheet to gray out the non-editable QLineEdit
        # self.current_modelname.setStyleSheet("background-color: white; height: 40px; font-size: 16pt; color: #36454F;")
        self.current_modelname.setDisabled(True)
        
        # --------------------------------------------------

        self.new_model_label = QLabel("New Model Name")
        self.new_model_label.setObjectName("labelDialog")

        self.new_modelname = QLineEdit()
        self.new_modelname.setPlaceholderText("New modelname")
        self.setObjectName("editDialog")

        # self.new_modelname.setStyleSheet("height: 40px; font-size: 16pt;")

        self.new_modelname.textChanged.connect(self.check_username_exist)

        self.edit_mode_warning = QLabel()
        self.edit_mode_warning.hide()  
        self.edit_mode_warning.setObjectName("TMSWarningLabel") 

        # buttons_widget =  QWidget()
        # self.button_hbox =  QHBoxLayout(buttons_widget)
        # self.btn_cancel = QPushButton("Cancel")
        # self.update_btn = QPushButton("Update")
        # self.update_btn.setEnabled(False)
        # self.default_stylesheet_btn=  "background-color: #F8F8F8;"
        # self.update_btn.setStyleSheet(self.default_stylesheet_btn)

        # self.update_btn.setContentsMargins(0, 0, 0, 0)


        # self.update_btn.clicked.connect(self.submit_form)
        # self.btn_cancel.clicked.connect(self.reject)
        # self.button_hbox.addWidget(self.btn_cancel)
        # self.button_hbox.addWidget(self.update_btn)
        buttons_widget =  QWidget()
        self.button_hbox =  QHBoxLayout(buttons_widget)
        
        self.update_btn = QPushButton("Update")
        self.update_btn.setFixedSize(150, 40)
        self.update_btn.setStyleSheet("font-family: Calibri; font-size: 21px;font-weight:bold; color: #FFFFFF; background-color: #C2222E;border:none")
        self.update_btn.clicked.connect(self.submit_form)
        


        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedSize(150, 40)
        self.btn_cancel.setStyleSheet("font-family: Calibri; font-size: 21px;font-weight:bold; color: #C2222E; background-color: #FFFFFF;border:1px solid #C2222E")
        self.btn_cancel.clicked.connect(self.reject)
        self.button_hbox.addWidget(self.btn_cancel)
        self.button_hbox.addWidget(self.update_btn)


        self.form_layout.addWidget(self.header_label)
        self.form_layout.addSpacing(15)

        self.form_layout.addWidget(self.current_model_label)
        self.form_layout.addWidget(self.current_modelname)
        self.form_layout.addWidget(self.new_model_label)
        self.form_layout.addWidget(self.new_modelname)

        self.form_layout.addWidget(self.edit_mode_warning)
        self.form_layout.addStretch(1)

        self.form_layout.addWidget(buttons_widget)

        self.setLayout(self.form_layout)

    def check_username_exist(self):
        new_model_name = self.new_modelname.text()
        old_model_name = self.current_modelname.text()
        self.flag_new_username_used = False
        dbList = self.TMS_repo.get_model_list(model_name=new_model_name)

        if len(new_model_name) < 4:
            self.edit_mode_warning.setText("Modelname should have a minimum of 4 characters.")
            self.edit_mode_warning.show() 
        elif new_model_name == old_model_name:
            self.edit_mode_warning.setText("Modelname is same as current modelname")
            self.edit_mode_warning.show() 
        elif any(item['modelName'] == new_model_name for item in dbList): 
            self.edit_mode_warning.setText("Model name already exists ")
            self.edit_mode_warning.show() 
            self.flag_new_username_used = False
        else:
            self.edit_mode_warning.hide() 
            self.flag_new_username_used = True
        self.enable_submit_button()

    def enable_submit_button(self):
        if self.flag_new_username_used:
            # self.update_btn.setStyleSheet("background-color: #50C878;")
            self.update_btn.setEnabled(True)
            self.update_btn.setCursor(Qt.PointingHandCursor)
        else:
            self.update_btn.setStyleSheet(self.default_stylesheet_btn)
            self.update_btn.setEnabled(False)
 
    def submit_form(self):
        new_model_name = self.new_modelname.text()
        if new_model_name :
            is_updated = self.TMS_repo.edit_model_details(self.model_id,new_model_name,self.session_user)
            if is_updated : 
                print("After updating modelname query")
                self.pop_up_success_message("Model name Updated Successfully")
            else :
                print("Failed Update modelname")
                self.pop_up_failure_message("Model name Update Failed")
            self.after_model_edited.emit()
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

#     window =ModelUpdateDialogBox('PINg24',21)
#     window.show()

#     app.exec()