
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys
import os.path
import math
from pathlib import Path
from functools import partial


run_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(run_path)
sys.path.append(run_path)

# from TMS_pages.table_icon_widget import IconWidget
from ui.user_add_widget import UserAddDialogBox
from repository.masterdb import AdminDatabaseManager
from ui.custom_table_TMS_widget import CustomTableWidget
from ui.update_password_widget import  PasswordUpdateDialogBox
from ui.update_username_widget import  UsernameUpdateDialogBox

class UserListWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(" USERS LIST")

        window = QMainWindow()
        window.setObjectName("app")
        self.image_path = "assets/images/"
        self.setWindowIcon(QIcon(self.image_path+'app_icon.png'))
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: black;")
        self.image_path = "assets/images/"
        # central_widget.setFont(QFont("Poppins", 12, QFont.Normal))
        window.setCentralWidget(central_widget)
        
        self.main_vertical_layout = QVBoxLayout(central_widget)
        new_user_btn =  self.add_user_push_button()
        self.main_vertical_layout.addWidget(new_user_btn, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        #  ----------------------------
        header_widget = QWidget()
        header_widget.setFixedHeight(50) 
        self.header_layout = QHBoxLayout(header_widget)
        #show
        self.show_label = QLabel("Show:")
        self.show_label.setFixedWidth(50)
        self.header_layout.addWidget(self.show_label)
        #dropdown for no of items
        self.rows_per_page_combo = QComboBox()
        self.rows_per_page_combo.addItems(["10", "25", "50", "100"])
        self.rows_per_page_combo.setFixedSize(50, 25)
        self.header_layout.addWidget(self.rows_per_page_combo)
        #label
        self.entries_label=QLabel("entries")
        self.header_layout.addWidget(self.entries_label)
        #search label
        self.search_label=QLabel("Search:")
        self.search_label.setFixedSize(60, 20)
        self.search_label.setAlignment(Qt.AlignRight)
        self.header_layout.addWidget(self.search_label)
        #search bar
        self.search_line_edit = QLineEdit()
        self.search_line_edit.setFixedSize(200, 25)
        self.header_layout.addWidget(self.search_line_edit)      
    
        self.main_vertical_layout.addWidget(header_widget)

        #  -------------------------
        # Create controls for pagination and search
        self.pagination_layout = QHBoxLayout()
        self.page_label = QLabel()
        self.prev_button = QPushButton("Previous")
        self.prev_button.setStyleSheet("color: blue;")
        self.prev_button.setFixedWidth(70)
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("color: blue;")
        self.next_button.setFixedWidth(70)
        self.page_navigation_layout = QHBoxLayout()
        self.pagination_layout.addWidget(self.page_label)
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addLayout(self.page_navigation_layout)
        self.pagination_layout.addWidget(self.next_button)
        self.main_vertical_layout.addLayout(self.pagination_layout)
        
        self.column_headings = ["Employee Id", "Username", "Account Type",'Update Username', "Update Password"]
        
        self.table_widget = CustomTableWidget()
        self.current_page =1
        self.rows_per_page = 10
        row_height = 50 
        self.table_widget.setHorizontalHeaderLabels(self.column_headings)
        self.table_widget.verticalHeader().setDefaultSectionSize(row_height)
        self.load_data()
        self.display_table()
        self.setup_table()

         # Connect signals
        self.rows_per_page_combo.currentIndexChanged.connect(self.update_table)
        self.prev_button.clicked.connect(self.prev_page)
        self.next_button.clicked.connect(self.next_page)
        self.search_line_edit.textChanged.connect(self.search_table)

        self.main_vertical_layout.addWidget(self.table_widget)
        self.main_vertical_layout.setAlignment(Qt.AlignTop)
        
        self.setLayout(self.main_vertical_layout)

    def on_user_add_clicked(self):
        # QMessageBox.information(self,"Add User Clicked","Not enabled yet")
        self.dialog_box = UserAddDialogBox()
        self.dialog_box.add_new_user_signal.connect(self.reload_data)
        self.dialog_box.exec()



    def add_user_push_button(self):
        new_user_btn = QPushButton("Add New User")
        new_user_btn.setObjectName('new_user')
        new_user_btn.setStyleSheet('#new_user {background-color: white;font-family: Calibri;font-size: 11pt;font-weight: bold;border: 0.5px solid white;color: #C2222E;}')
        new_user_btn.setFixedSize(169, 42)
        new_user_btn.setCursor(Qt.PointingHandCursor)

        # # Set the text and icon for the button
        # new_user_btn.setText()
        plus_icon = QIcon(self.image_path+"add_user.png")  # Replace "path_to_plus_icon.png" with the actual path to your plus icon
        new_user_btn.setIcon(plus_icon)
        new_user_btn.setIconSize(QSize(24,24))
        new_user_btn.clicked.connect(self.on_user_add_clicked)
        return new_user_btn


    def load_data(self):
        # Simulated data loading
        self.data = []
        self.userList = {}
        self.admin_db = AdminDatabaseManager()
        self.admin_db.connect()
        self.userList['data'] = self.admin_db.get_user_details()
        if self.userList is not None:
            self.data = self.userList['data']
        # print(self.data)
        inputListData = []

        if self.data is not None:
            for i in self.data:
                # machineData[i['id']] = {"name":i['machineName'],'plcIP':i['plcIp'],'systemIP':i['systemIp'],'successImg':i['successImage'],'failureImg':i['failureImage'],'warningImg':i['warningImage'],'amsIP':i['amsIp'],'statusFlag':i['statusFlag']}
                input={'employeeId':i['employeeId'], 'userName':i['userName'],'accountType':i['role'],'updateUsername': 'Update  Username','updatePassword' : 'Update Password'}
                inputListData.append(input)
        self.data = inputListData
        # for i in range(1, 128):
        #     self.data.append([f"1.{i}", f"2.{i}", f"3.{i}", f"4.{i}", f"5.{i}", f"6.{i}", f"7.{i}"])


    
    def display_table(self):
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = min(start_idx + self.rows_per_page, len(self.data))
        self.table_widget.setRowCount(end_idx - start_idx)
        self.colHeaders = ['employeeId', 'userName', 'accountType', 'updateUsername', 'updatePassword']
        text_font_size = 12
        text_font_family = 'roboto'
        for row, data_idx in enumerate(range(start_idx, end_idx)):
            for col, header in enumerate(self.colHeaders):
                background_color = "#ffffff" if row % 2 == 0 else "#EFEFEF"
                if col == 3:
                    edit_username_label = QLabel("Edit Username")
                    edit_username_label.setAlignment(Qt.AlignCenter)
                    edit_username_label.setCursor(Qt.CursorShape.PointingHandCursor)
                    # print(f"######## {self.data[data_idx]['userName']} ")
                    edit_username_label.mousePressEvent = partial(self.show_edit_username_dialog, self.data[data_idx]['userName'],self.data[data_idx]['employeeId'])   
                    edit_username_label.setStyleSheet(f'background-color: {background_color} ;font-family: {text_font_family}; font-size: {text_font_size}; color: blue;')
                    self.table_widget.setCellWidget(row, col, edit_username_label)
                if col == 4 :
                    edit_username_label = QLabel("Edit Password")
                    edit_username_label.setAlignment(Qt.AlignCenter)
                    edit_username_label.setCursor(Qt.CursorShape.PointingHandCursor)
                    # print(f"######## {self.data[data_idx]['userName']} ")
                    edit_username_label.mousePressEvent = partial(self.show_edit_password_dialog, self.data[data_idx]['userName'])   
                    edit_username_label.setStyleSheet(f'background-color: {background_color} ;font-family: roboto; font-size: 12pt; color: blue;')
                    self.table_widget.setCellWidget(row, col, edit_username_label)
                else:
                    item = QTableWidgetItem(str(self.data[data_idx][header]))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item.setBackground(QColor(background_color))
                    item_font = QFont()
                    item_font.setFamily(text_font_family)  
                    item_font.setPointSize(text_font_size)    
                    # font.setBold(True)       
                    item.setFont(item_font)
                    self.table_widget.setItem(row, col, item)

        # # Set alternating row colors
        # for row in range(self.table_widget.rowCount()):
        #     background_color = QColor("#fce3e5") if row % 2 == 0 else QColor("#ffffff")
        #     for col in range(self.table_widget.columnCount()):
        #         try:
        #             item = self.table_widget.item(row, col)
        #             if item:
        #                 item.setBackground(background_color)
        #         except AttributeError:  # If QLabel widget is present
        #             widget = self.table_widget.cellWidget(row, col)
        #             widget.setStyleSheet(f'background-color: {background_color}; font-family: roboto; font-size: 10pt; color: blue;')


        self.page_label.setText(f"Showing {start_idx + 1} to {end_idx} of {len(self.data)} entries")

    def show_edit_password_dialog(self,username ,event):
        print(f"Username passed to show_edit_password_dialog(): {username}")
        self.password_update = PasswordUpdateDialogBox(username)
        self.password_update.show()  
        self.password_update.after_password_updated.connect(self.reload_data) 


    def show_edit_username_dialog(self,username ,emp_id,event):
        print(f"Username passed to show_edit_password_dialog(): {username} ,empid : {emp_id}")
        self.username_update = UsernameUpdateDialogBox(username,emp_id)
        self.username_update.show() 
        self.username_update.after_username_updated.connect(self.reload_data) 
        

    def setup_table(self):
        self.table_widget.clear()
        self.table_widget.setRowCount(self.rows_per_page)
        self.table_widget.setColumnCount(5)

        # Set column headings
        self.table_widget.setHorizontalHeaderLabels(self.column_headings)
        row_height = 50  # Adjust this value to your preferred row height
        self.table_widget.verticalHeader().setDefaultSectionSize(row_height)

        self.display_table()
        self.update_page_navigation()

    def reload_data(self):
        self.load_data()
        self.setup_table()

    def update_table(self):
        self.rows_per_page = int(self.rows_per_page_combo.currentText())
        self.current_page = 1
        self.setup_table()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.setup_table()

    def next_page(self):
        if self.current_page < len(self.data) // self.rows_per_page + 1:
            self.current_page += 1
            self.setup_table()


    def keyPressEvent(self, event):
        self.admin_db.disconnect()
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def search_table(self):
        search_text = self.search_line_edit.text().strip().lower()
        self.load_data() 
        if search_text:
            filtered_data = []
            for row in self.data:
                for item in row.values():
                    if search_text in str(item).lower():
                        filtered_data.append(row)
                        break 
            self.data = filtered_data
        self.current_page = 1
        self.setup_table()
    
    def go_to_page(self, page):
        self.current_page = page
        self.setup_table()
    

    def update_page_navigation(self):
        # Clear the layout by removing all items
        while self.page_navigation_layout.count():
            item = self.page_navigation_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        page_count = math.ceil(len(self.data) / self.rows_per_page)
        max_pages_to_show = 3  

        if page_count <= max_pages_to_show:
            pages_to_display = list(range(1, page_count + 1))
        else:
            half_max = max_pages_to_show // 2
            if self.current_page - half_max <= 1:
                pages_to_display = list(range(1, max_pages_to_show + 1)) # for first 2 pages
            elif self.current_page + half_max >= page_count: # for pages 3 to 3rd last
                pages_to_display = list(range(page_count - max_pages_to_show + 1, page_count + 1))
            else: # for last 2 pages
                pages_to_display = list(range(self.current_page - half_max, self.current_page + half_max + 1))

        if 1 not in pages_to_display:
            pages_to_display.insert(0, 1) 
            if 2 not in pages_to_display:
                pages_to_display.insert(1, "...") 

        if page_count not in pages_to_display:
            if page_count - 1 not in pages_to_display:
                pages_to_display.append("...") 
            pages_to_display.append(page_count) 

        # Adding first button
        first_button = QPushButton("First")
        first_button.clicked.connect(partial(self.go_to_page, 1))
        first_button.setStyleSheet("color: blue;")
        first_button.setCursor(Qt.PointingHandCursor)
        first_button.setFixedWidth(60)
        self.page_navigation_layout.addWidget(first_button)
        # Adding number buttons
        for page in pages_to_display:
            if page == "...":
                self.label = QLabel("...")
            else:
                self.label = QPushButton(str(page))
                self.label.setCursor(Qt.PointingHandCursor)
                self.label.clicked.connect(partial(self.go_to_page, page))
            self.label.setStyleSheet("color: blue;")
            self.label.setFixedWidth(30)
            self.page_navigation_layout.addWidget(self.label)
            if page == self.current_page:
                self.label.setStyleSheet("background-color: grey;")
            else:
                self.label.setStyleSheet("color: blue;")
        # Adding last button
        last_button = QPushButton("Last")
        last_button.clicked.connect(partial(self.go_to_page, page_count))
        last_button.setStyleSheet("color: blue;")
        last_button.setCursor(Qt.PointingHandCursor)
        last_button.setFixedWidth(60)
        self.page_navigation_layout.addWidget(last_button)

        # Setting enable n disable for navigation buttons
        if self.current_page == 1:
            self.prev_button.setDisabled(True)
            self.prev_button.setCursor(Qt.ArrowCursor)
            self.prev_button.setStyleSheet("color: grey;")
            first_button.setDisabled(True)
            first_button.setCursor(Qt.ArrowCursor)
            first_button.setStyleSheet("color: grey;")
        else:
            self.prev_button.setDisabled(False)
            self.prev_button.setCursor(Qt.PointingHandCursor)
            self.prev_button.setStyleSheet("color: blue")
            first_button.setDisabled(False)
            first_button.setCursor(Qt.PointingHandCursor)
            first_button.setStyleSheet("color: blue")

        if self.current_page == page_count:
            self.next_button.setDisabled(True)
            self.next_button.setCursor(Qt.ArrowCursor)
            self.next_button.setStyleSheet("color: grey;")
            last_button.setDisabled(True)
            last_button.setCursor(Qt.ArrowCursor)
            last_button.setStyleSheet("color: grey;")
        else:
            self.next_button.setDisabled(False)
            self.next_button.setCursor(Qt.PointingHandCursor)
            self.next_button.setStyleSheet("color: blue")
            last_button.setDisabled(False)
            last_button.setCursor(Qt.PointingHandCursor)
            last_button.setStyleSheet("color: blue")


if __name__ == '__main__':
    app =  QApplication(sys.argv)
    
    # APP
    # window = ButtonDemo()
    window = UserListWidget()
  

    window.showMaximized()

    # EVENT LOOP
    app.exec()


