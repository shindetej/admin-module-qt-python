
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys,json
import os.path
import math,random
from pathlib import Path
from functools import partial

run_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(run_path)
sys.path.append(run_path)


# from TMS_pages.table_icon_widget import IconWidget
from ui.role_add_widget import RoleAddWidget
from ui.custom_table_TMS_widget import CustomTableWidget
from repository.masterdb import AdminDatabaseManager

from ui.iconwidget import IconWidget
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


class RolePermissionWidget(QWidget):
    
    def __init__(self):

        # LOGGER MODULE SETUP
        logs.logJson['ModuleName']="RolePermissionMapping"
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']
        logs.logJson['Endpoint']="TMSApp"


        #  CODE
        super().__init__()
        logger.info(f"Widget Name: {os.path.basename(os.path.abspath(__file__))}; starts here")
        self.setWindowTitle("ROLE-PERMISSION MAPPING TABLE")
        window = QMainWindow()
        window.setObjectName("app")

        # ICON
        self.image_path ="assets/images/"
        self.setWindowIcon(QIcon(self.image_path+'app_icon.png'))

        # DATABASE CONNECTION
        self.TMS_admin_db = AdminDatabaseManager()
        self.TMS_admin_db.connect()
        
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        self.main_vertical_layout = QVBoxLayout(central_widget)

        self.button_group = QWidget()
        self.btn_group_layout = QHBoxLayout(self.button_group)

        # BUTTON GROUP  
        self.update_permission_btn = self.add_push_button_click(button_name="Update Role-Permissions",on_click_routine=self.update_role_permissions,button_width=280,hide_button_flag=True)
        self.btn_group_layout.addWidget(self.update_permission_btn)

        self.add_role_btn = self.add_push_button_click(button_name="Add New Role",on_click_routine=self.add_new_role,button_width=175,button_icon=self.image_path+"add_user.png")
        self.btn_group_layout.addWidget(self.add_role_btn)

        
        #  ----------------------------
        self.table_widget = CustomTableWidget()
        self.load_data()
        self.setup_table()

        self.main_vertical_layout.addWidget(self.button_group,alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.main_vertical_layout.addWidget(self.table_widget)
         
        self.main_vertical_layout.setAlignment(Qt.AlignTop)        
        self.setLayout(self.main_vertical_layout)

    def add_push_button_click(self, button_name=None,button_icon=None,object_name='new_model',on_click_routine=None,button_width=175,button_height=42,hide_button_flag=False,point_cursor_flag=True):
        custom_button_add = QPushButton(button_name)
        custom_button_add.setObjectName(object_name)
        custom_button_add.setStyleSheet('#new_model {background-color: white;font-family: Calibri;font-size: 11pt;font-weight: bold;border: 0.5px solid white;color: #C2222E;}')
        custom_button_add.setFixedSize(button_width, button_height)

        if button_icon :
            plus_icon = QIcon(button_icon)  # Replace "path_to_plus_icon.png" with the actual path to your plus icon
            custom_button_add.setIcon(plus_icon)
            custom_button_add.setIconSize(QSize(24,24))

        if point_cursor_flag:
            custom_button_add.setCursor(Qt.PointingHandCursor)

        if  hide_button_flag :
            custom_button_add.hide()

        if on_click_routine:
            custom_button_add.clicked.connect(on_click_routine)
            return custom_button_add

    def load_data(self):
       
        self.update_permissions_final_data = {}
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="load_data"
        logs.logJson['Message']="Inside load_data()"
        logger.info(logs.logJson) 
        try:
            self.data = []
            self.permission_list = {}
            self.column_headings = ["Permissions"]
            self.role_name_list =  self.TMS_admin_db.get_role_name_list()
            for role in self.role_name_list : 
                    self.column_headings.append(role['roleName'])
            # self.column_headings.append(self.role_name_list['roleName']+"("+self.role_name_list['roleId']+")")
            

            self.current_page =1
            # self.rows_per_page = 10
            row_height = 50 
            # self.table_widget.setColumnCount(len(self.column_headings))
            self.table_widget.setHorizontalHeaderLabels(self.column_headings)
            self.table_widget.verticalHeader().setDefaultSectionSize(row_height)

            #  get permissions list
            self.permission_list = json.loads(self.TMS_admin_db.get_permission_list())
            if self.permission_list['statusCode'] == 200 : 
                self.data = self.permission_list['data']
                
            # get permissions assigned to all roles
            
            self.permissions_list_by_role = {}
            for role in self.role_name_list : 
                self.permissions_list_by_role[role['roleName']] = self.TMS_admin_db.get_permissions_associated_with_roleid(role['roleId'])
            self.rows_per_page=len(self.data)
            inputListData = []

            if self.data is not None:
                for i in self.data:
                    input={'permission':i['permissionName']+"("+i['permissionCode']+")"}
                    for role in self.role_name_list :

                        # if 1st cell has permission code which exists in given role's permission list then set true 
                        if i['permissionCode'] in self.permissions_list_by_role[role['roleName']]:
                                input[role['roleName']] = True
                        else :
                                input[role['roleName']] = False
                    inputListData.append(input)

            self.data = inputListData

          

        except Exception as e :
            exception_type, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    def display_table(self):
        logger.info(f"\n### INSIDE DISPLAY_TABLE ###")

        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="display_table"
        logs.logJson['Message']="Inside display_table()"
        logger.info(logs.logJson) 
        try:
            start_idx = (self.current_page - 1) * self.rows_per_page
            end_idx = min(start_idx + self.rows_per_page, len(self.data))
            self.table_widget.setRowCount(end_idx - start_idx)

            self.colHeaders = list(self.data[0].keys())
        
            logger.info("Table Display Rendered")
            text_font_size = 12
            text_font_family = 'roboto'
            
            for row, data_idx in enumerate(range(start_idx, end_idx)):
                for col, header in enumerate(self.colHeaders):
                    if col == 0 :
                        item = QTableWidgetItem(str(self.data[data_idx][header]))
                        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                        item_font = QFont()
                        item_font.setFamily(text_font_family)  
                        item_font.setPointSize(text_font_size)    
                        item.setFont(item_font)
                        self.table_widget.setItem(row, col, item)
                    else :
                        check_widget = QWidget()
                        checkbox = self.add_checkbox()
                        checkbox.setChecked(self.data[data_idx][header])
                        layout = QHBoxLayout(check_widget)

                         # on state changed of check box
                        role_of_checkbox = self.table_widget.horizontalHeaderItem(col).text()
                        permission_of_checkbox = self.table_widget.item(row,0).text()
                      
                      
                        checkbox.stateChanged.connect(partial(self.checkbox_changed,role_col=role_of_checkbox,permission_row=permission_of_checkbox))
                        layout.addWidget(checkbox)
                        layout.setAlignment(checkbox, Qt.AlignCenter)  # Align checkbox to center
                        self.table_widget.setCellWidget(row, col, check_widget)
            # self.page_label.setText(f"Showing {start_idx + 1} to {end_idx} of {len(self.data)} entries")
        except Exception as e :
            exception_type, exception_value, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    def add_checkbox(self):
        chk_box = QCheckBox()
        TMS_check = self.image_path + "TMS_check.png"
        TMS_uncheck = self.image_path + "TMS_radio.png"
        chk_box.setStyleSheet(f"""
                                QCheckBox {{ spacing: 35px; }} 
                                QCheckBox::indicator {{ width: 35px; height: 30px; }} 
                                QCheckBox::indicator:checked {{ image : url({TMS_check}); }} 
                                QCheckBox::indicator:unchecked {{ image : url({TMS_uncheck}); }} 
                                """)
        chk_box.setCursor(Qt.PointingHandCursor)
        return chk_box
    
    def checkbox_changed(self,state,role_col,permission_row):
        logger.info(f"\n### INSIDE CHECKBOX_CHANGED ###")
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="checkbox_changed"
        logs.logJson['Message']="Inside checkbox_changed()"
        logger.info(logs.logJson) 

         # on state changed of check box
        #2. update dictionary
            #2.1. if state changed to 0 remove permission code from dictionary
            #2.2. if state changed to 2 add permission code to dictionary
       
        permission = permission_row.split("(")[1].split(")")[0].strip()
        if state == 2:
            if permission not in self.permissions_list_by_role[role_col]:
                self.permissions_list_by_role[role_col].append(permission)
        else :
            if permission in self.permissions_list_by_role[role_col]:
                self.permissions_list_by_role[role_col].remove(permission)
                logger.info(f"updated permission after remove {permission} : {self.permissions_list_by_role[role_col]} ")
        self.update_permission_btn.show()
        
    def setup_table(self):
        logger.info(f"\n### INSIDE SETUP_TABLE ###")
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="setup_table"
        logs.logJson['Message']="Inside setup_table()"
        logger.info(logs.logJson)

        self.table_widget.clear()
        self.table_widget.setRowCount(self.rows_per_page)
        self.table_widget.setColumnCount(len(self.column_headings))

        # Set column headings
        self.table_widget.setHorizontalHeaderLabels(self.column_headings)
        row_height = 50  # Adjust this value to your preferred row height
        self.table_widget.verticalHeader().setDefaultSectionSize(row_height)

        self.display_table()
        self.update_permission_btn.hide()
        
    def reload_data(self):
        logger.info(f"\n### INSIDE RELOAD_DATA ###")
        
        self.load_data()
        self.setup_table()
    
    def update_role_permissions(self):

        #3. update respective permission codes to role assigned in db
            #3.1 delete existing role permission mapping for particular role id
            #3.1 Insert new role permission mapping for that role id
        logger.info(f"In UPDATE_ROLE_PERMISSIONS() ::: {self.permissions_list_by_role} ")
        # {'admin': ['CUSR', 'EUSR'], 'operator': ['CUSR', 'VUSR', 'DUSR'], 'executive': ['CUSR', 'VUSR', 'DUSR']} 
        count = self.TMS_admin_db.assign_permissions_for_role_id(self.permissions_list_by_role,created_by="Jr Dev")
        logger.info(f"TOTAL UPDATED RECORDS : {count}")
        self.pop_up_success_message("Updated Permissions Successfully")
        self.reload_data()

    def add_new_role(self):
        logger.info("Inside add_new_role()")
        self.role_add_box = RoleAddWidget()
        self.role_add_box.show() 
        self.role_add_box.after_adding_new_role.connect(self.reload_data)
  

    def pop_up_success_message(self,message):
        self.mb =  CustomDialog(message,status_file.successStatusCode)
        self.mb.exec()
 

    def pop_up_failure_message(self,message):
        self.mb =  CustomDialog(message,status_file.errorMsg)
        self.mb.exec()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.TMS_admin_db.disconnect()
            self.close()
    
   
    # def add_new_push_button(self,button_name="button name"):
    #     custom_button_add = QPushButton(button_name)
    #     custom_button_add.setObjectName('new_model')
    #     custom_button_add.setStyleSheet('#new_model {background-color: white;font-family: Calibri;font-size: 11pt;font-weight: bold;border: 0.5px solid white;color: #C2222E;}')
    #     custom_button_add.setFixedSize(175, 42)
    #     custom_button_add.setCursor(Qt.PointingHandCursor)

    #     # # Set the text and icon for the button
    #     # custom_button_add.setText()
    #     plus_icon = QIcon(self.image_path+"add_user.png")  # Replace "path_to_plus_icon.png" with the actual path to your plus icon
    #     custom_button_add.setIcon(plus_icon)
    #     custom_button_add.setIconSize(QSize(24,24))
    #     return custom_button_add

if __name__ == '__main__':
    app =  QApplication(sys.argv)
    
    # APP
    # window = ButtonDemo()
    window = RolePermissionWidget()
  

    window.showMaximized()

    # EVENT LOOP
    app.exec()


