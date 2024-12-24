import sys ,os ,json
from PySide6.QtWidgets import *
run_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(run_path)
print(f"******* {run_path}")
from PySide6.QtCore import Qt, QSize,QTimer,QDate
from PySide6.QtGui import *
sys.path.append(run_path)

print(f"\n-------\nRUN PATH APPENDED TO SYSTEM : {run_path}")

from repository.masterdb import AdminDatabaseManager
from ui.user_list_management import UserListWidget
from ui.model_list_widget import ModelListWidget
from ui.role_permission_widget import RolePermissionWidget
from utilities.CustomSplashScreen  import CustomSplashScreen 




# -------- LOGGER ---------------
from logs import logs
import logging,random
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



class TMSLoginScreen(QWidget):
    def __init__(self, label_name):
        # LOGGER
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside TMSLoginScreen()"
        logs.logJson['Tag']="TMSLoginScreen"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson)

        # CODE
        super().__init__()
        self.admin_db =  AdminDatabaseManager()    
        self.image_path = os.path.join(run_path, "assets", "images/")

        self.setWindowIcon(QIcon(self.image_path+"app_icon.png"))

        self.width_of_label = 24
        self.width_of_edit = 500
        self.height_of_label = 26
        self.height_of_edit = 40

        # Create the label
        self.logo_on_login = QLabel()
        pixmap_logo= QPixmap(self.image_path+"myicon.png")
        pixmap_logo = pixmap_logo.scaled(200, 150, Qt.KeepAspectRatio)
        self.logo_on_login.setPixmap(pixmap_logo)
        self.logo_on_login.setAlignment(Qt.AlignCenter)


        self.label_login = QLabel("Login")
        self.label_login.setFixedSize(200, 35)
        self.label_login.setAlignment(Qt.AlignCenter)
        self.label_login.setStyleSheet("font-family: sans serif;font-size: 21pt; color: #D51D2A; ")
        self.label_login.setContentsMargins(0, 0, 0, 0)


        username_widget = self.__login_username_widget("user.png","Username",self.width_of_label,self.height_of_label,self.width_of_edit,self.height_of_edit)
        password_widget = self.__login_password_widget("padlock.png","Password",self.width_of_label,self.height_of_label,self.width_of_edit,self.height_of_edit)
       
        vbox_login_layout =  QVBoxLayout()
        vbox_login_layout.addWidget(self.logo_on_login,alignment=Qt.AlignCenter)
        vbox_login_layout.addSpacing(30)
        vbox_login_layout.addWidget(self.label_login,alignment=Qt.AlignCenter)
        vbox_login_layout.addSpacing(30)
        vbox_login_layout.addWidget(username_widget)
        vbox_login_layout.addWidget(password_widget)
        vbox_login_layout.setAlignment(Qt.AlignCenter)


        self.hbox_forgot_password =  QHBoxLayout()

         # Create the label
        self.label_invalid_creds = QLabel("Wrong Login Credentials !!")
        self.label_invalid_creds.setFixedSize(262, 24)
        self.label_invalid_creds.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignVCenter)
        self.label_invalid_creds.setStyleSheet("font-family: sans serif;font-size: 11pt; color: red")
        self.label_invalid_creds.setContentsMargins(0, 0, 0, 0)
        self.label_invalid_creds.setVisible(False)
        self.hbox_forgot_password.addWidget(self.label_invalid_creds)
        
    
         # Create the label
        self.label_forgot_password = QLabel("Forgot password?")
        self.label_forgot_password.setFixedSize(162, 24)
        self.label_forgot_password.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label_forgot_password.setStyleSheet("font-family: sans serif;font-size: 11pt; color: #0057FF;")
        self.label_forgot_password.setContentsMargins(0, 0, 0, 0)
        self.label_forgot_password.setCursor(Qt.PointingHandCursor)
        self.label_forgot_password.mousePressEvent = self.forgot_password_clicked
        self.hbox_forgot_password.addWidget(self.label_forgot_password,alignment=Qt.AlignmentFlag.AlignRight)

    
        forgot_password_widget = QWidget()
        forgot_password_widget.setLayout(self.hbox_forgot_password)

        vbox_login_layout.addWidget(forgot_password_widget)

        login_btn =  QPushButton("Login")
        login_btn.setObjectName('login_btn')
        login_btn.setStyleSheet('#login_btn {background-color: #D51D2A;font-family: Calibri;font-size: 14pt;font-weight: bold;border: 0.5px solid #D51D2A;color:white;}')
        login_btn.setFixedSize(563, 60)
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.clicked.connect(self.on_login_clicked)
        
        # Add the login_btn to the QVBoxLayout vbox_layout_for_complete_form
        vbox_login_layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        
        login_widget = QWidget()
        login_widget.setFixedSize(675,638)
        login_widget.setObjectName("loginUser")
        login_widget.setStyleSheet("#loginUser {background-color: #FFFFFF;border: 1px solid white;border-radius: 10px;}")
        login_widget.setLayout(vbox_login_layout)

     
        vbox_main_layout =  QVBoxLayout()
        vbox_main_layout.addSpacing(105)
        vbox_main_layout.addWidget(login_widget,alignment=Qt.AlignCenter)

        self.footer_widget = QWidget()
        self.footer_layout = QHBoxLayout(self.footer_widget)
        copy_right = QLabel(f"Copyright ©{QDate.currentDate().year()} by Tejas Demo LLC All Rights Reserved.")
        copy_right.setStyleSheet("font-size: 12pt; color: #73746B;" )
        self.footer_layout.addSpacing(20)
        self.footer_layout.addWidget(copy_right,alignment=Qt.AlignCenter)
        self.footer_layout.addSpacing(20)
        vbox_main_layout.addWidget(self.footer_widget)

        self.setLayout(vbox_main_layout)
    
 

    def __login_username_widget(self,icon_path,placeholder_message,width_of_label,height_of_label,width_of_edit,height_of_edit):
        efield_hbox = QHBoxLayout()    
        efield_hbox.setSpacing(0)     
        
        label_username = QLabel()
        pixmap_efield= QPixmap(self.image_path+icon_path)
        pixmap_efield = pixmap_efield.scaled(width_of_label, height_of_label, Qt.KeepAspectRatio)
        label_username.setPixmap(pixmap_efield)
        label_username.setFixedSize(width_of_label, height_of_label)
        label_username.setAlignment(Qt.AlignCenter)
 

        self.ledit_username = QLineEdit()
        self.ledit_username.setFixedSize(QSize(width_of_edit, height_of_edit))
        self.ledit_username.setPlaceholderText(placeholder_message)
        self.ledit_username.setStyleSheet("QLineEdit { border: none; background-color: white; padding: 5px; font-family: Verdana;font-size: 16pt; } "
                                "QLineEdit::hover { background-color: white; } "
                                "QLineEdit::focus { background-color: white; }")

        efield_hbox.addWidget(label_username)
        efield_hbox.addSpacing(5)
        efield_hbox.addWidget(self.ledit_username)
        efield_hbox.addStretch(3)

        widget_width =563
        widget_height = 74
        
        edit_field_widget = QWidget()
        edit_field_widget.setLayout(efield_hbox )
        edit_field_widget.setFixedSize(widget_width,widget_height)
        edit_field_widget.setObjectName("efield")
        edit_field_widget.setStyleSheet("#efield {background-color: white;border: 1px solid #D51D2A}")
        return edit_field_widget
    
    def __login_password_widget(self,icon_path,placeholder_message,width_of_label,height_of_label,width_of_edit,height_of_edit):
        efield_hbox = QHBoxLayout()    
        efield_hbox.setSpacing(0)     
        
        label_efield = QLabel()
        pixmap_efield= QPixmap(self.image_path+icon_path)
        pixmap_efield = pixmap_efield.scaled(width_of_label, height_of_label, Qt.KeepAspectRatio)
        label_efield.setPixmap(pixmap_efield)
        label_efield.setFixedSize(width_of_label, height_of_label)
        label_efield.setAlignment(Qt.AlignCenter)
 

        self.ledit_pwd = QLineEdit()
        self.ledit_pwd.setFixedSize(QSize(width_of_edit, height_of_edit))
        self.ledit_pwd.setPlaceholderText(placeholder_message)
        self.ledit_pwd.setStyleSheet("QLineEdit { border: none; background-color: white; padding: 5px; font-family: Verdana;font-size: 16pt; } "
                                "QLineEdit::hover { background-color: white; } "
                                "QLineEdit::focus { background-color: white; }")

        efield_hbox.addWidget(label_efield)
        efield_hbox.addSpacing(5)
        efield_hbox.addWidget(self.ledit_pwd)
        efield_hbox.addStretch(3)

        self.label_eye = QLabel()   
        self.label_eye.setFixedSize(width_of_label, height_of_label)
        self.label_eye.setAlignment(Qt.AlignCenter)
        self.label_eye.setCursor(Qt.PointingHandCursor)
        self.set_visual_state(False)
        
            # Connect the mousePressEvent to the toggle_visual_state function
        self.mousePressEvent = self.toggle_visual_state
        efield_hbox.addWidget(self.label_eye)


        widget_width =563
        widget_height = 74
        
        edit_field_widget = QWidget()
        edit_field_widget.setLayout(efield_hbox )
        edit_field_widget.setFixedSize(widget_width,widget_height)
        edit_field_widget.setObjectName("efield")
        edit_field_widget.setStyleSheet("#efield {background-color: white;border: 1px solid #D51D2A}")
        return edit_field_widget
    
    def forgot_password_clicked(self,event):
        QMessageBox.information(self,"Admin message","Please contact admin to reset password",)

    def on_login_clicked(self):
        # QMessageBox.information(self,"Login Clicked","Not enabled yet")
        username =  self.ledit_username.text()
        password =  self.ledit_pwd.text()     
        self.admin_db.connect()

        login_data = self.admin_db.check_login(username,password)
        
        if  login_data  :
            print(f"logged in data {login_data}")
            print (f"dict : {json.loads(login_data)}")

            login_json_to_dict= json.loads(login_data)

            login_status = login_json_to_dict['statusCode']
            
            if login_status == 200 : 
                login_data_dict= json.loads(login_json_to_dict['data'])
                user_role  = login_data_dict['roleName']
                self.splash = CustomSplashScreen(self.image_path+'TMS_splash.gif', Qt.WindowStaysOnTopHint)
                self.splash.show()
                if user_role.lower() == "admin":
                    self.window_main = UserListWidget()
                    QTimer.singleShot(2000,self.finishSplash)     
                if user_role == "operator":       
                    self.window_main = ModelListWidget()
                    QTimer.singleShot(500,self.finishSplash)         
                if user_role == "Executive":       
                    self.window_main = RolePermissionWidget()
                    QTimer.singleShot(500,self.finishSplash)         
            else :
                print("Invalid creds !!")
                self.show_label_for_duration(self.label_invalid_creds,3000)
        else :
            self.show_label_for_duration(self.label_invalid_creds,3000)
            

        

    def show_label_for_duration(self,label_var,timing_in_msec):
        # Create a QTimer object
        label_var.setVisible(True)
        timer = QTimer(self)
        timer.setSingleShot(True)  
        timer.timeout.connect(lambda: self.__hide_invalid_creds_label(label_var)) 
        timer.start(timing_in_msec)  

    # Method to hide the label
    def __hide_invalid_creds_label(self,label_var):
        label_var.setVisible(False)

    def finishSplash(self):
        self.splash.finish(self.window_main)
        self.splash.close()
        self.window_main.showMaximized()
        # self.window_main.integrated_dashboard_app.actions1[0].trigger()
        self.close()   
    def set_visual_state(self, is_visual):
        if is_visual:
            self.pixmap_eye= QPixmap(self.image_path+"eye-off.png")
            # self.pixmap_eye= QPixmap("show.png")
            self.ledit_pwd.setEchoMode(QLineEdit.EchoMode.Normal)            
        else:
            # self.pixmap_eye= QPixmap("visual.png") 
            self.pixmap_eye= QPixmap(self.image_path+"eye_TMS.png") 
            self.ledit_pwd.setEchoMode(QLineEdit.EchoMode.Password)
            
        self.pixmap_eye = self.pixmap_eye.scaled(24, 26, Qt.KeepAspectRatio)
        self.label_eye.setPixmap(self.pixmap_eye)
        

    
    def toggle_visual_state(self, event):
        # Toggle the visual state and update the image
        self.is_visual = not getattr(self, 'is_visual', False)
        self.set_visual_state(self.is_visual)


    
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.admin_db.disconnect()
            self.close()
        if event.key() == Qt.Key_Return:
            print("Enter Pressed")
            self.on_login_clicked()

    

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # APP
    # window = ButtonDemo()
    window = TMSLoginScreen("Login Screen")
    window.setWindowTitle("TMS Pin Inspection")
    window.showMaximized()

    # EVENT LOOP
    app.exec()