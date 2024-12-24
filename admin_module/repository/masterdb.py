import json
import sys,random
import os.path
from pathlib import Path
import psycopg2
from pathlib import Path

# logging.basicConfig(filename=str(Path(pathlog).parent) + "/logs/TMS_system.log",format='%(message)s',filemode='a')
# pathlog = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(str(Path(pathlog).parent))
run_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(run_path)
sys.path.append(run_path)

print(f"\n-------\nRUN PATH APPENDED TO SYSTEM : {run_path}")
from utilities.AuthorizationUtils import AuthorizationUtils



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



"""@Author : 1503
Class used to manage TMS database related queries for CRUD Operation"""

class TMSDatabaseManager:
    config = None

    def __init__(self):
        self.initialize_config()        
        self.connection = None
        self.cursor = None
        logs.logJson['ModuleName']="TMSDatabaseManager"
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']



    @staticmethod
    def load_db_config():
        try:
            current_file_directory = os.path.dirname(os.path.abspath(__file__))
            # print(f"{os.path.dirname(current_file_directory)}"+'/config.json')
            config_file_path = os.path.dirname(current_file_directory)+'/resources/config.json'
            print(f"CONFIG FILE PATH : {config_file_path}")
            with open(config_file_path) as f:
                return json.load(f)
        except Exception as e:
            print("Error loading configuration:", e)

    @staticmethod
    def initialize_config():
        if TMSDatabaseManager.config is None:
            TMSDatabaseManager.config = TMSDatabaseManager.load_db_config()

    def connect(self):
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        
        logs.logJson['Tag']="TMSDatabaseManager"
        logs.logJson['Message']= "Inside connect()"
        logger.info(logs.logJson) 
        try:
            if self.connection is None : 
                self.connection = psycopg2.connect(
                    user=TMSDatabaseManager.config['DBConfig']['User'],
                    password=TMSDatabaseManager.config['DBConfig']['Password'],
                    host=TMSDatabaseManager.config['DBConfig']['Host'],
                    port=TMSDatabaseManager.config['DBConfig']['Port'],
                    database=TMSDatabaseManager.config['DBConfig']['DBName']
                )
                self.cursor = self.connection.cursor()
                self.connection.autocommit = True
                print(f"Database connect success !!! ")
        except Exception as e:
            print("Failed to connect to database:", e)

    def disconnect(self):
        try:
           if self.cursor is not None and not self.cursor.closed: 
            self.cursor.close()
           if self.connection is not None and not self.connection.closed:
            self.connection.close()
            print("Disconnected from Database !!!")
        except Exception as e:
            print("Error while disconnecting from database:", e)

    # ---------- Model CRUD  ------------
    # Add New Model
    def add_model(self, model_name, created_by=None ):
        # logger
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside add_model()"
        logs.logJson['Tag']="add_model"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson)

        # code
        if created_by is None:
            created_by = "NA"
       
        print(f"New Model Details :\n'model name : {model_name}',created_by : {created_by},")
        # try:
        query = f"insert into public.TMS_model_master(model_name, is_enabled, is_deleted, created_by, created_date, updated_by, updated_date) values(%s, true, false, %s, CURRENT_TIMESTAMP,%s , CURRENT_TIMESTAMP);"
        # self.cursor.execute(query)
        query_params = (model_name,created_by,created_by)
        return self.insert_query_execution(query=query,query_params=query_params)
        
    
    def insert_query_execution(self, query, query_params):
        # logger
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside insert_query_execution()"
        logs.logJson['Tag']="insert_query_execution"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson)

        # code
        try:
            self.cursor.execute(query, query_params)
            print(f"Query executed: {query}")
            logger.info(f"Query executed >>>")
            if self.cursor.rowcount:
                logger.info(f"Successfully no. of rows inserted: {self.cursor.rowcount}")
            return self.cursor.rowcount
        except Exception as e:
            print("Exception occurred while executing query:", e)
            # Log the exception details if needed
            exception_type, exc_obj, exc_tb = sys.exc_info()
            filename = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            print(f"File name: {filename}")
            logger.info(f"Exception occurred while executing query: {e}")
            logger.info(f"Exception Type : {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return 0
    #  # Add New Model OLD 
    # def add_model(self, model_name, created_by=None ):
    #     if created_by is None:
    #         created_by = "NA"
       
    #     print(f"New Model Details :\n'model name : {model_name}',created_by : {created_by},")
    #     try:
    #         query = f"insert into public.TMS_model_master(model_name, is_enabled, is_deleted, created_by, created_date, updated_by, updated_date) values('{model_name}', true, false, '{created_by}', CURRENT_TIMESTAMP,'{created_by}' , CURRENT_TIMESTAMP);"
    #         self.cursor.execute(query)
        
    #         print(f"Model Insert Query  : {query}")
           
    #         if self.cursor.rowcount :
    #             print(f"No of rows inserted : {self.cursor.rowcount} ")
    #         return self.cursor.rowcount
     
    #     except Exception as e:
    #         print("Exception occurred while adding model:" +  str(e))
    #         exception_type, exception_object, exception_traceback = sys.exc_info()
    #         filename = exception_traceback.tb_frame.f_code.co_filename
    #         line_number = exception_traceback.tb_lineno 
    #         logger.info(f"Exception type: {exception_type}")
    #         logger.info(f"File name: {filename}")
    #         logger.info(f"Line number:{line_number}")
    #         logger.info(Exception(e))
    #         return 0
        
     # Edit Model
    def edit_model_details(self,model_id, new_model_name,updated_by=None):
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside edit_model_details()"
        logs.logJson['Tag']="edit_model_details"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson) 
        if updated_by is None:
            created_by = "NA"
        if model_id is not None and new_model_name is not None :
            print(f"Update user details : {new_model_name}")
            try:
                query = f"update public.TMS_model_master set model_name = '{new_model_name}' ,updated_by = '{updated_by}', updated_date = current_timestamp where model_id = '{model_id}' ;"
                 # Check if the update was successful
                
                self.cursor.execute(query)
                if self.cursor.rowcount > 0:
                    print(f"Update query successfully updated entry for id {model_id}")
                else:
                    print(f"No rows were affected by the update query for id {model_id}")
                
                return self.cursor.rowcount
            
            except Exception as e:
                print("Exception occurred while editing model name:" +  str(e))
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))
                return 0
        
     # Soft delete Model
    def delete_model_by_id(self,model_id,updated_by = None ):
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside delete_model_by_id()"
        logs.logJson['Tag']="delete_model_by_id"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson) 
        if updated_by is None:
            created_by = "NA"
        if model_id is not None  :
            try:
                query = f"update public.TMS_model_master set is_deleted = True, updated_by = '{updated_by}', updated_date = current_timestamp where model_id = {model_id} ;"
                 # Check if the update was successful
                print(f"Query : {query}")
                self.cursor.execute(query)
                if self.cursor.rowcount > 0:
                    print(f"count is not 0")
                    print(f"Deleted model with id : {model_id}")
                else:
                    print(f"count is zero")
                    print(f"No rows were affected by the delete query for id {model_id}")
                
                return self.cursor.rowcount
            except Exception as e:
                print("Exception occurred while delete model by id:" +  str(e))
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))
                return 0
    # Get Model List
    def get_model_list(self,model_name = None,model_id = None,order_by ='model_id',order_type = 'asc'):
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside get_model_list()"
        logs.logJson['Tag']="get_model_list"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson) 
        model_result_table =[]
        query_string = ''
        order_string = f" ORDER BY {order_by} {order_type};"
        if  model_id :
            print("model id appended to query string")
            query_string += f" and model_id = {model_id}"
        if  model_name : 
            print("model name appended to query string")
            query_string += f" and model_name = '{model_name}'"
        try : 
            query = "select model_id , model_name from public.TMS_model_master where 1=1 and is_deleted = false " +query_string +order_string+";"
            self.cursor.execute(query)
            print(f"executed query : {query} ")

            result =self.cursor.fetchall()
            print(f"result collected")

            # columns = [desc[0] for desc in self.cursor.description]
            # print(f"Result {result}")
            for row in result:
                row_entry = {}
                row_entry['modelId'] = row[0]
                row_entry['modelName'] = row[1]
                model_result_table.append(row_entry)
            print(f"ROWS : {model_result_table}")
            return model_result_table 
        except Exception as e:
            print("Exception occurred while get model details:" +  str(e))
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))  
            
    
    

    # ---------- Defect and Bin CRUD  ------------
        
     # Add New Defect
    def add_defect(self,defect_type, inspect_criteria,cat_no,bin_id, created_by=None ):
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="add_defect"
        logs.logJson['Message']= "Inside add_defect()"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson)
        if created_by is None:
            created_by = "NA"
       
        print(f"New Defect Details :\n'defect_type : {defect_type}',inspect_criteria : {inspect_criteria},cat no : {cat_no}',bin_id : {bin_id},created_by : {created_by},")
        query = f"insert into public.TMS_defect_master(defect_type, inspection_criteria, category_no, is_enabled, is_deleted, created_by, created_date, updated_by, updated_date, bin_id) values(%s, %s, %s, true, false,%s , current_timestamp, %s, current_timestamp, %s);"

        query_params_for_add_defect = (defect_type,inspect_criteria,cat_no,created_by,created_by,bin_id)
        return self.insert_query_execution(query=query,query_params=query_params_for_add_defect)


    #  Get Defect Details
    def get_defect_details_list(self,defect_id=None,bin_id = None,defect_type = None,order_by ='adm.defect_id',order_type = 'desc' ):
        
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="get_defect_details_list"
        logs.logJson['Message']= "Inside get_defect_details_list()"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson)
        defect_result_table =[]
        query_string = ''
        order_string = f" ORDER BY {order_by} {order_type};"
        if  defect_id is not None:
            print("defect id appended to query string")
            query_string += f" and adm.defect_id  = {defect_id}"
        if  bin_id is not None : 
            print("bin no appended to query string")
            query_string += f" and adm.bin_id = {bin_id}"
        if  defect_type is not None: 
            print("defect type appended to query string")
            query_string += f" and adm.defect_type   = '{defect_type}'"
        
        try : 
            query = "select adm.defect_id , adm.defect_type , adm.inspection_criteria , adm.category_no , abm.action_status , adm.bin_id , abm.bin_color , abm.dimension , abm.quantity from TMS_defect_master adm inner join TMS_bin_master abm on adm.bin_id = abm.bin_id where 1=1 and adm.is_deleted = false " +query_string +order_string+";"
            self.cursor.execute(query)
            print(f"executed query : {query} ")

            result =self.cursor.fetchall()
            print(f"result collected")

            # columns = [desc[0] for desc in self.cursor.description]
            # print(f"Result {result}")
            for row in result:
                row_entry = {}
                row_entry['defectId'] = row[0]
                row_entry['defectType'] = row[1]
                row_entry['inspectionCriteria'] = row[2]
                row_entry['catNo'] = row[3]
                row_entry['actionStatus'] = row[4]
                row_entry['binId'] = row[5]
                row_entry['binColor'] = row[6]
                row_entry['dimension'] = row[7]
                row_entry['binQuantity'] = row[8]
                defect_result_table.append(row_entry)
            print(f"ROWS : {defect_result_table}")
            return defect_result_table
    
        except Exception as e:
            print("Exception occurred while get defect details:" +  str(e))
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
        
   
     # Edit Defect
    def edit_defect_details(self,defect_id,defect_type, inspect_criteria,cat_no,bin_id,updated_by=None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside edit_defect_details()"
        logs.logJson['Tag']="edit_defect_details"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson)
        if updated_by is None:
            created_by = "NA"
        if defect_type  and bin_id and inspect_criteria and cat_no :
            print(f"Update user details : {defect_type}")
            try:
                query = f"update public.TMS_defect_master set defect_type = '{defect_type}', inspection_criteria = '{inspect_criteria}', category_no = '{cat_no}', updated_by = '{updated_by}', updated_date = current_timestamp , bin_id = {bin_id} where defect_id = {defect_id};"
                 # Check if the update was successful
                
                self.cursor.execute(query)
                if self.cursor.rowcount > 0:
                    print(f"Update query successfully updated entry for id {defect_id}")
                else:
                    print(f"No rows were affected by the update query for id {defect_id}")
                
                return self.cursor.rowcount
            except Exception as e:
                print("Exception occurred while editing defect name:" +  str(e))
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))
                return 0
            
        

    def get_bin_details(self,action_status=None,binId=None ):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="get_bin_details"
        logger.info(logs.logJson)

        bin_result_table =[]
        query_string = ''

        if  action_status is not None: 
            print("defect type appended to query string")
            query_string += f" and action_status   = '{action_status}'"
        if  binId is not None: 
            print("defect type appended to query string")
            query_string += f" and bin_id   = {binId}"
        try : 
            query = "select action_status , bin_id , bin_color , dimension , quantity from TMS_bin_master abm where 1 = 1 and is_deleted = false " +query_string +";"
            self.cursor.execute(query)
            print(f"executed query : {query} ")

            result =self.cursor.fetchall()
            print(f"result collected")

            # columns = [desc[0] for desc in self.cursor.description]
            # print(f"Result {result}")
            for row in result:
                row_entry = {}
                row_entry['actionStatus'] = row[0]
                row_entry['binId'] = row[1]
                row_entry['binColor'] = row[2]
                row_entry['binDim'] = row[3]
                row_entry['binQty'] = row[4]
                bin_result_table.append(row_entry)
            print(f"ROWS : {bin_result_table}")
            return bin_result_table
        
        except Exception as e:
            print("Exception occurred while get bin details:" +  str(e))
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return bin_result_table
        

    def get_action_details(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="get_action_details"
        action_result_table = []
        try : 
            query = "select concat(action_status ,'(',bin_id ,')') as action from TMS_bin_master"
            self.cursor.execute(query)
            print(f"executed query : {query} ")

            result =self.cursor.fetchall()
            print(f"result collected")

            # columns = [desc[0] for desc in self.cursor.description]
            # print(f"Result {result}")
    
            for row in result:
                action_result_table.append(row[0])
            print(f"ROWS : {action_result_table}")
            return action_result_table
    
        except Exception as e:
            print("Exception occurred while get action on bin details:" +  str(e))
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return action_result_table
        
    def delete_defect_by_id(self,defect_id,updated_by = None ):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Tag']="delete_defect_by_id"
        if updated_by is None:
            created_by = "NA"
        if defect_id is not None  :
            try:
                query = f"update public.TMS_defect_master set is_deleted = True, updated_by = '{updated_by}', updated_date = current_timestamp where defect_id = {defect_id} ;"
                 # Check if the update was successful
                print(f"Query : {query}")
                self.cursor.execute(query)
                if self.cursor.rowcount > 0:
                    print(f"count is not 0")
                    print(f"Deleted model with id : {defect_id}")
                else:
                    print(f"count is zero")
                    print(f"No rows were affected by the delete query for id {defect_id}")
                
                return self.cursor.rowcount
          
            except Exception as e:
                print("Exception occurred while delete defect details:" +  str(e))
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))
                return 0

    

"""@Author : 1503
Class used to manage admin database related queries for CRUD Operation"""
class AdminDatabaseManager:
    config = None

    def __init__(self):
        self.initialize_config()        
        self.connection = None
        self.cursor = None

        logs.logJson['ModuleName']="AdminDatabaseManager"
        logs.logJson['SelfProcessTag']=logs.logJson['ProcessId']+"_" + logs.logJson['ModuleName']
        logs.logJson['Endpoint']="TMSApp"

    @staticmethod
    def load_db_config():
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside load_db_config()"
        logs.logJson['Tag']="load_db_config"
        logger.info(logs.logJson)
        try:
            current_file_directory = os.path.dirname(os.path.abspath(__file__))
            # print(f"{os.path.dirname(current_file_directory)}"+'/config.json')
            config_file_path = os.path.dirname(current_file_directory)+'/resources/config.json'
            print(f"CONFIG FILE PATH : {config_file_path}")

            with open(config_file_path) as f:
                return json.load(f)
        except Exception as e:
            
            print("Exception occurred while load_db_config:" +  str(e))
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return 0

    @staticmethod
    def initialize_config():
        if AdminDatabaseManager.config is None:
            AdminDatabaseManager.config = AdminDatabaseManager.load_db_config()
            print(f"Configuration loaded::: ")

    def connect(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside admin connect()"
        logs.logJson['Tag']="connect"
        logger.info(logs.logJson)
        print(f"Inside connect : : ")
        # print(f"User : {AdminDatabaseManager.config['DBConfig']['User']}")
        # print(f"Password : {AdminDatabaseManager.config['DBConfig']['Password']}")
        # print(f"Host : {AdminDatabaseManager.config['DBConfig']['Host']}")
        # print(f"Port : {AdminDatabaseManager.config['DBConfig']['Port']}")
        # print(f"DBConfig : {AdminDatabaseManager.config['DBConfig']['DBName']}")
        
        try:
            if self.connection is None : 
                self.connection = psycopg2.connect(
                    user=AdminDatabaseManager.config['DBConfig']['User'],
                    password=AdminDatabaseManager.config['DBConfig']['Password'],
                    host=AdminDatabaseManager.config['DBConfig']['Host'],
                    port=AdminDatabaseManager.config['DBConfig']['Port'],
                    database=AdminDatabaseManager.config['DBConfig']['DBName']
                )
                self.cursor = self.connection.cursor()
                self.connection.autocommit = True
                print("Connected to Database")
        
        except Exception as e:
            print("Exception occurred while get defect details:" +  str(e))
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return 0

    def disconnect(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside disconnect()"
        logs.logJson['Tag']="disconnect"
        logger.info(logs.logJson)
        try:
           if self.cursor is not None and not self.cursor.closed: 
            self.cursor.close()
           if self.connection is not None and not self.connection.closed:
            self.connection.close()
            print("Disconnected from Database")
        except Exception as e:
            print("Error while disconnecting from database:", e)

    ###########  USER CRUD ############
    
    # Add New User
    def add_user(self, username, first_name, last_name,employee_id, password,role_id, created_by=None ):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside add_user()"
        logs.logJson['Tag']="add_user"
        logger.info(logs.logJson)
        if created_by is None:
            created_by = "dev team"
        hashed_password = AuthorizationUtils.generate_hashed_password(password)
        print(f"New User Details :\n'user name : {username}'\nfirst_name : {first_name}\n'last_name : {last_name}'\nemployee_id : {employee_id}\n created_by : {created_by},")
        try:
            query = '''
                INSERT INTO TMS_admin.adm_users ( username, first_name, last_name,employee_id, hashed_password, is_enabled, is_deleted, created_by, created_date, updated_by, updated_date) 
                VALUES( %s, %s, %s,%s, %s,  TRUE, FALSE, %s, CURRENT_TIMESTAMP, %s, CURRENT_TIMESTAMP) RETURNING user_id ;
            '''
            self.cursor.execute(query, (username, first_name,last_name,employee_id,hashed_password,created_by,created_by))
            user_id = self.cursor.fetchone()[0]
            if user_id :
                print(f"User Id {user_id}")
                if user_id : 
                    self.assign_role_to_user_id(user_id,role_id)
            logs.logJson['Message'] = f"User {username}({user_id}) Added Successfully"
            logger.info(logs.logJson)
        except Exception as e:
            print("Exception occurred while adding user:", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    # Edit Username
    def edit_username_of_existing_user(self,employeeId, username,updated_by ):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside edit_username_of_existing_user()"
        logs.logJson['Tag']="edit_username_of_existing_user"
        logger.info(logs.logJson)  
        if employeeId is not None and username is not None :
            print(f"Update user details : {username}")
            try:
                query = '''
                    UPDATE TMS_admin.adm_users set username =%s, updated_by =%s, updated_date = CURRENT_TIMESTAMP where employee_id = %s and is_deleted = false;
                '''
                 # Check if the update was successful
                
                self.cursor.execute(query, (username, updated_by,employeeId))
                if self.cursor.rowcount > 0:
                    print(f"Update query successfully updated entry for id {employeeId}")
                else:
                    print(f"No rows were affected by the update query for id {employeeId}")
                
                return self.cursor.rowcount
            except Exception as e:
                print("Exception occurred while editing username of user:", e)
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))
                return 0
    
    # Edit Password
    def edit_password_of_user(self,username , updated_password,updated_by ):
            logs.logJson['UniqueValue']= str(random.randint(0, 999999))
            logs.logJson['Message']= "Inside edit_password_of_user()"
            logs.logJson['Tag']="edit_password_of_user"
            logger.info(logs.logJson)  
            if username  and updated_password :
                new_hashed_password = AuthorizationUtils.generate_hashed_password(updated_password)

                print(f"Update User Details : New Password Hashed{new_hashed_password}") 
                try:
                    query = '''
                        UPDATE TMS_admin.adm_users SET hashed_password=%s, updated_by=%s, updated_date = CURRENT_TIMESTAMP  WHERE username =  %s;
                    '''
                    self.cursor.execute(query, (new_hashed_password, updated_by,username))
                    print(f"Password updated successfully for {username}")
                    if self.cursor.rowcount > 0:
                        print(f"Update query successfully updated entry for id {username}")
                    else:
                        print(f"No rows were affected by the update query for id {username}")
                
                    return self.cursor.rowcount
                except Exception as e:
                    print("Exception occurred while editing password of user:", e)
                    return 0
            else :
                print("Invalid Username or New Password!!")
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))
                return 0
    
    def edit_user_details(self, employeeId, username, password, updated_password, updated_by=None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside edit_user_details()"
        logs.logJson['Tag']="edit_user_details"
        logger.info(logs.logJson)  
        if updated_by  is None:
            updated_by='admin_dev'

        if employeeId  :
            if username :
                # Edit Username
                print(f"Update user details: {username}")
                query_username = '''
                    UPDATE TMS_admin.adm_users SET username=%s, updated_by=%s, updated_date = CURRENT_TIMESTAMP WHERE employee_id = %s;
                '''
                self.cursor.execute(query_username, (username, updated_by, employeeId))
                print(f"Username updated successfully for {employeeId}")

            if password :
                # Edit Password
                login_data = self.__get_user_login_data(username)
                b_result = AuthorizationUtils.verify_password(password, login_data['hashedKey'])

                if b_result:
                    new_hashed_password = AuthorizationUtils.generate_hashed_password(updated_password)

                    print(f"Update User Details: New Password Hashed{new_hashed_password}")
                    query_password = '''
                        UPDATE TMS_admin.adm_users SET hashed_password=%s, updated_by=%s, updated_date = CURRENT_TIMESTAMP WHERE employee_id = %s;
                    '''
                    self.cursor.execute(query_password, (new_hashed_password, updated_by, employeeId))
                    print(f"Password updated successfully for {username}")
                else:
                    print("Invalid Current Credentials, Re-Enter Password!!")
            else:
                print("Invalid username or password!!")
        else:
            print("Invalid employeeId or updated_by!!")
            



    def get_username_list(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside get_username_list()"
        logs.logJson['Tag']="get_username_list"
        logger.info(logs.logJson)
        list_of_users = []

        try : 
            query = "select au.username from TMS_admin.adm_users au where au.is_deleted = false"
            self.cursor.execute(query)
            print(f"executed")

            result =self.cursor.fetchall()
            print(f"result collected")

            # columns = [desc[0] for desc in self.cursor.description]
            # print(f"Result {result}")
            for row in result:
                username  = row[0]
                list_of_users.append(username)
            print(f"list of users : {list_of_users}")
            return list_of_users
        except Exception as e :
            print("Exception occurred while get user details:", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return list_of_users

    # Get User Details in list
    def get_user_details(self,userid=None,username=None,first_name=None,employee_id=None,role_name=None,order_by=None,order_type=None):
        quert_string = " "
        order_string =  " "
        try : 
            query = '''select au.user_id, au.username, au.first_name, au.last_name, au.employee_id, ar.role_name from TMS_admin.adm_users au left join TMS_admin.adm_user_role_assoc aura on au.user_id = aura.user_id left join TMS_admin.adm_roles ar on ar.role_id = aura.role_id where 1 = 1 and au.is_deleted = false '''

            if userid is not None :
                quert_string += f" and au.user_id = {userid}"
                query += quert_string

            if username is not None :
                quert_string += f" and au.username = '{username}'"
                query +=  quert_string

            if first_name is not None :
                quert_string += f" and au.first_name = {first_name}"
                query += quert_string

            if employee_id is not None :
                quert_string += f" and au.employee_id = {employee_id}"
                query += quert_string

            if role_name is not None :
                quert_string += f" and ar.role_name = {role_name}"
                query += quert_string

            if order_by is not None:
                if order_type is None :
                     order_string += f" ORDER BY {order_by} asc;"
                else :
                     order_string += f" ORDER BY {order_by} desc;"
            else:
                if order_type is None :
                     order_string += f" ORDER BY user_id  asc"
                else :
                     order_string += f" ORDER BY user_id  desc"

            
            query += order_string
            print(f"QUERY : {query}")

            self.cursor.execute(query)
            print(f"executed")

            result =self.cursor.fetchall()
            print(f"result collected")

            list_of_rows = []
            # columns = [desc[0] for desc in self.cursor.description]
            # print(f"Result {result}")
            for row in result:
                row_entries = {}
                row_entries['userId'] = row[0]
                row_entries['userName'] = row[1]
                row_entries['fullName'] = row[2] + " " +row[3]
                row_entries['employeeId'] = row[4] 
                row_entries['role'] = row[5] 
                # print("RESULT IN FUNCTION :"+str(dict(zip(columns, row))))
                # print(f"ROW ENTRY  f{row_entries}")
                list_of_rows.append(row_entries)
            
            return list_of_rows
    
        except Exception as e :
            print("Exception occurred while get user details:", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    # GET Login Response Data
    def __get_user_login_data(self,username):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside __get_user_login_data()"
        logs.logJson['Tag']="__get_user_login_data"
        logger.info(logs.logJson)
        on_login_data =  {} 
        try : 
            if username is not None : 
                query =  f"select au.hashed_password,ar.role_id,ar.role_name,au.username,concat(au.first_name ,' ',au.last_name) as name,au.employee_id  from TMS_admin.adm_users au inner join TMS_admin.adm_user_role_assoc aura on au.user_id = aura.user_id inner join TMS_admin.adm_roles ar on aura.role_id = ar.role_id where au.is_deleted = false and au.username = '{username}'"
                # query =  f"select hashed_password from TMS_admin.adm_users where is_deleted = false and username = '{username}'"
                print(f"QUERY : {query}")
                self.cursor.execute(query)

                result_row = self.cursor.fetchone()
                if result_row is not None:
                    print(f"1222")

                    on_login_data['hashedKey'] = result_row[0]
                    on_login_data['roleId'] = result_row[1]
                    on_login_data['roleName'] = result_row[2]
                    on_login_data['username'] = result_row[3]
                    on_login_data['name'] = result_row[4]
                    on_login_data['employeeId'] = result_row[5]
                    return on_login_data
                else :
                    on_login_data['errorMessage'] = f"Invalid username {username}!"
                    return on_login_data
            else :
                print("Username is None  ")
                on_login_data['errorMessage'] = f"Invalid username {username}!"
                return on_login_data


                
        except Exception as e :
            on_login_data['errorMessage']= f"Invalid username "
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            print(f"login data printed {on_login_data}")
            return on_login_data


    def check_login(self,username,password):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside check_login()"
        logs.logJson['Tag']="check_login"
        logger.info(logs.logJson)
        #  check empty condtion for username and password
        if not username or not password:
            print("Username or password is not entered")
            return None
        response_json ={}  
        try:
            print("Inside check_login()")
            login_data  = self.__get_user_login_data(username=username)
            print(f"login data in check login() ")
            if 'errorMessage' in login_data:
                print("User not found")
                response_json = {
                    'statusCode': 404,
                    'data': None
                }
                response_json = json.dumps(response_json)
                print(f"response json : {response_json}")
                return response_json 
            else :
                print("User found")
                response_json['statusCode'] = 404
                b_result = AuthorizationUtils.verify_password(password,login_data['hashedKey'])
                print(f"verify result: {b_result}")
                #  modify json
                del login_data['hashedKey']
                response_json = {}
                if b_result:
                    print("Login Successful!!!")
                    print(f"role of user logged in : {login_data['roleName']}")
                    permissionsList = self.get_permissions_associated_with_roleid(login_data['roleId'])
                    login_data['permissions'] =  permissionsList
                    login_data = json.dumps(login_data)
                    response_json['statusCode'] = 200
                    response_json['data'] = login_data
                    

                else :
                    login_data['loginStatus'] = b_result
                    response_json['statusCode'] = 404
                    response_json['data'] = None
                    
                response_json = json.dumps(response_json)
                return response_json

        except Exception as e:
            print("Exception occurred while check_login():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            print(f"Exception type: {exception_type}"+   f"....Line number:{line_number}")
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return None

    ###########  PERMISSION CRUD ############
    
    def get_permission_list(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "get_permission_list check_login()"
        logs.logJson['Tag']="get_permission_list"
        logger.info(logs.logJson)
        try : 
            query =  f"select ap.permission_id as \"permissionId\", ap.permission_code as \"permissionCode\", ap.permission_name as \"permissionName\", ap.description from TMS_admin.adm_permissions ap where ap.is_enabled = true and ap.is_deleted = false"
            print(f"QUERY : {query}")
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            columns = [desc[0] for desc in self.cursor.description]
            json_perm_list = []
            for row in result:
                row_dict = dict(zip(columns, row)) 
                json_perm_list.append(row_dict)
                json_final = {
                    'data' : json_perm_list,
                    'statusCode' : 200
                }

            json_repsonse = json.dumps(json_final)

            print(f"\n\n\nPermission List to return : {json_repsonse}")
            return json_repsonse
  
        except Exception as e :
            print("Exception occurred while get_permission_list():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))


    def get_permission_id_for_code(self, permission_code_list):
        try:
            # Log the operation
            logs.logJson['UniqueValue'] = str(random.randint(0, 999999))
            logs.logJson['Message'] = "get_permission_list check_login()"
            logs.logJson['Tag'] = "get_permission_list"
            logger.info(logs.logJson)
            
            # Prepare the SQL query with parameterized query to prevent SQL injection
            query = "SELECT ap.permission_id AS permissionId FROM TMS_admin.adm_permissions ap WHERE ap.is_enabled = true AND ap.is_deleted = false AND ap.permission_code IN (%s)"
            placeholders = ', '.join(['%s' for _ in permission_code_list])
            query = query % placeholders
            
            # Execute the query with parameterized values
            self.cursor.execute(query, permission_code_list)
            
            # Fetch the results
            result = self.cursor.fetchall()
            
            # Extract permission IDs from the result
            perm_id_list = [row[0] for row in result]
            
            # Log the permission IDs to be returned
            logger.info(f"Permission IDs to return: {perm_id_list}")
            
            return perm_id_list
  
        except Exception as e :
            print("Exception occurred while get_permission_list():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return None

    def add_new_permission(self,permission_name,permission_code,description,created_by=None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In add_new_permission()"
        logs.logJson['Tag']="add_new_permission"
        logger.info(logs.logJson)
        try : 
            if permission_name  and permission_code is not None :
                if created_by is None : 
                    created_by = "Not Provided"
                query = '''
                    insert into TMS_admin.adm_permissions(permission_name, permission_code, is_enabled, is_deleted, created_by, created_date, updated_by, updated_date, description) values(%s, %s, true, false, %s, CURRENT_TIMESTAMP, %s, CURRENT_TIMESTAMP, %s);
                '''
                self.cursor.execute(query, (permission_name, permission_code,created_by,created_by,description))
                print("Permission added successfully .")
  
        except Exception as e :
            print("Exception occurred while add_new_permission():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
    
    def update_permission_details(self,permission_id ,permission_code=None ,permission_name=None,description=None,updated_by=None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In update_permission_details()"
        logs.logJson['Tag']="update_permission_details"
        logger.info(logs.logJson)
        # print(f"permission_id : {permission_id} ,permission_name={permission_name},description={description},updated_by={updated_by}")
        if permission_id :
            query =  f"select ap.permission_id as \"permissionId\", ap.permission_code as \"permissionCode\", ap.permission_name as \"permissionName\", ap.description from TMS_admin.adm_permissions ap where ap.permission_id = {permission_id} and ap.is_deleted = false"
            print(f"QUERY : {query}")
            self.cursor.execute(query)
         
            result_row = self.cursor.fetchone()
            if result_row is not None :
                print(f"Printing result permission by id : {result_row}")
                if permission_code is None :
                    permission_code =  result_row[1]
                if permission_name is None :
                    permission_name =  result_row[2]
                if description is None :
                    description =  result_row[3]
                if updated_by is None : 
                    updated_by = "Not Available"
            print(f"Update permission details for permission id {permission_id}")
            try:
                query = f"update TMS_admin.adm_permissions set permission_name = '{permission_name}', permission_code = '{permission_code}', description = '{description}', updated_by = '{updated_by}', updated_date = current_timestamp where permission_id = {permission_id} and is_deleted = false; "
                print(f"QUERY UPDATE: set permission_name = '{permission_name}', permission_code = '{permission_code}', description = '{description}', updated_by = '{updated_by}', updated_date = current_timestamp where permission_id = {permission_id}")
                
                self.cursor.execute(query)
                print(f"Permission updated successfully for id {permission_id}")
            except Exception as e:
                print("Exception occurred while editing permission:", e)
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))
        
    ###########  ROLE CRUD ############

    def get_role_name_list(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In get_role_name_list()"
        logs.logJson['Tag']="get_role_name_list"
        logger.info(logs.logJson)
        list_of_roles = []
        try : 
            query = "select ar.role_id ,ar.role_name from TMS_admin.adm_roles ar where ar.is_deleted = false"
            self.cursor.execute(query)

            result =self.cursor.fetchall()

            # columns = [desc[0] for desc in self.cursor.description]
            # print(f"Result {result}")
            for row in result:
                row_entry = {}
                row_entry['roleId'] = row[0]
                row_entry['roleName'] = row[1]
                list_of_roles.append(row_entry)
            print(list_of_roles)
            return list_of_roles
        except Exception as e :
            print("Exception occurred while get role name list:", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return list_of_roles

    def get_role_details(self):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In get_role_details()"
        logs.logJson['Tag']="get_role_details"
        logger.info(logs.logJson)
        try : 
            query =  f"select ar.role_id as \"roleId\" , ar.role_name as \"roleName\" , ar.role_description as \"roleDesc\" from TMS_admin.adm_roles ar where ar.is_enabled = true and ar.is_deleted = false"
            print(f"QUERY : {query}")
            self.cursor.execute(query)
            # Fetch all the results into a list
            result = self.cursor.fetchall()

            # Convert the result to a list of dictionaries
            columns = [desc[0] for desc in self.cursor.description]
            json_role_list = []
            for row in result:
                row_dict = dict(zip(columns, row))  
                json_role_list.append(row_dict)
                json_final = {
                            'data' : json_role_list,
                            'statusCode' : 200}
            json_repsonse = json.dumps(json_final)

            print(f"\nRole List to return : {json_repsonse}")
            return json_repsonse
  
        except Exception as e :
            print("Exception occurred while get_role_list():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    def add_new_role(self,role_name,role_description,created_by=None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In add_new_role()"
        logs.logJson['Tag']="add_new_role"
        logger.info(logs.logJson)
        
        if role_name   and role_description  :
            if created_by is None : 
                created_by = "Not Provided"
            query = f" insert into TMS_admin.adm_roles(role_name, role_description, is_enabled, is_deleted, created_by, created_date, updated_by, updated_date) values(%s, %s, true, false, %s, CURRENT_TIMESTAMP,%s, CURRENT_TIMESTAMP);"
            return self.insert_query_execution(query=query,query_params=(role_name, role_description,created_by,created_by))
  

    def update_role_details(self,role_id ,role_name=None,role_description=None,updated_by= None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In update_role_details()"
        logs.logJson['Tag']="update_role_details"
        logger.info(logs.logJson)
        print(f"role_id = {role_id},role_name={role_name},role_description={role_description},updated_by= {updated_by})")
        if role_id :
            query =  f"select ar.role_id ,ar.role_name , ar.role_description from TMS_admin.adm_roles ar where ar.role_id = {role_id} and ar.is_deleted = false"
            print(f"QUERY : {query}")
            self.cursor.execute(query)
         
            result_row = self.cursor.fetchone()
            if result_row is not None :
                print(f"Printing result permission by id : {result_row}")
                if role_name is None :
                    role_name =  result_row[1]
                if role_description is None :
                    role_description =  result_row[2]
                if updated_by is None : 
                    updated_by = "Not Available"
            print(f"Update role details for permission id {role_id}")
            try:
                query = f"update TMS_admin.adm_roles set role_name = '{role_name}', role_description = '{role_description}', updated_by = '{updated_by}', updated_date = current_timestamp where role_id = {role_id} and is_deleted =false; "
                print(f"QUERY UPDATE: set role_name = '{role_name}' role_description = '{role_description}', updated_by = '{updated_by}', updated_date = current_timestamp where role_id = {role_id} ")
                
                self.cursor.execute(query)
                print(f"Role updated successfully for id {role_id}")
            except Exception as e:
                print("Exception occurred while updating role", e)
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno 
                logger.info(f"Exception type: {exception_type}")
                logger.info(f"File name: {filename}")
                logger.info(f"Line number:{line_number}")
                logger.info(Exception(e))

    def delete_role_with_mappings(self,role_id):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In delete_role_with_mappings()"
        logs.logJson['Tag']="delete_role_with_mappings"
        logger.info(logs.logJson)
        try : 
            res= self.get_role_by_id(role_id)
            if res:
                print("Role Id Exists")
                query = f"DELETE FROM TMS_admin.adm_role_permission_assoc WHERE role_id ={role_id};DELETE FROM TMS_admin.adm_user_role_assoc WHERE role_id = {role_id}; DELETE FROM TMS_admin.adm_roles WHERE role_id= {role_id};"
                # query = f"UPDATE TMS_admin.adm_roles SET is_deleted = true WHERE  role_id = {role_id};"
                print(query)
                self.cursor.execute(query)
                print("Role deleted successfully .")
            else :
                print("Required Positional Argument Are None")
       
        except Exception as e :
            print("Exception occurred while delete_role_with_mappings():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))


    def get_role_by_id(self,role_id):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In get_role_by_id()"
        logs.logJson['Tag']="get_role_by_id"
        logger.info(logs.logJson)
        try : 
            if role_id:
                query =  f"select role_id ,role_name from TMS_admin.adm_roles ar where is_deleted =false and role_id = {role_id}"
                print(f"QUERY : {query}")
                self.cursor.execute(query)
                result_row = self.cursor.fetchone()
                if result_row is not None :
                    return result_row
                else : 
                    return " Invalid Role Id"
            else :
                print("Role by id does not exist in database")
       
        except Exception as e :
            print("Exception occurred while get_role_by_name():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    
       
        except Exception as e :
            print("Exception occurred while get_role_by_name():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
    
    ###########  USER ROLE ASSOC ############
    def assign_role_to_user_id(self,user_id,role_id,created_by=None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In assign_role_to_user_id()"
        logs.logJson['Tag']="assign_role_to_user_id"
        logger.info(logs.logJson)
        try : 
            if user_id   and role_id  :
                if created_by is None : 
                    created_by = "NA"
                query = f" insert into TMS_admin.adm_user_role_assoc(user_id, role_id, is_enabled, is_deleted, created_by, created_date, updated_by, updated_date) values(%s, %s, true, false, %s, CURRENT_TIMESTAMP, %s, CURRENT_TIMESTAMP);"
                self.cursor.execute(query, (user_id, role_id,created_by,created_by))
                logs.logJson['Message']= (f"Role id {role_id} assigned to {user_id}  successfully .")
                logger.info(logs.logJson)
            else :
                print("Function parameters missing")
    
        except Exception as e :
            print("Exception occurred while add_new_role():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            
    ###########  PERMISSION ROLE ASSOC ############
    def get_permissions_associated_with_roleid(self,role_id):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In get_permissions_associated_with_roleid()"
        logs.logJson['Tag']="get_permissions_associated_with_roleid"
        logger.info(logs.logJson)
        try : 
            if role_id  : 
                query =  f"select ap.permission_code from TMS_admin.adm_permissions ap inner join TMS_admin.adm_role_permission_assoc arpa on ap.permission_id = arpa.permission_id inner join TMS_admin.adm_roles ar on arpa.role_id = ar.role_id where ar.role_id = '{role_id}'"
                print(f"QUERY : {query}")
                self.cursor.execute(query)
                # Fetch all the results into a list
                permissions = [row[0] for row in self.cursor.fetchall()]
                print(f"Permission List to return : {permissions}")
                return permissions
            else :
                print("Invalid role id")
                return None
                
        except Exception as e :
            print("Exception occurred while get_permissions_associated_with_roleid():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    def assign_permissions_for_role_id(self,permission_role_dict,created_by=None):
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "In assign_permissions_for_role_id()"
        logs.logJson['Tag']="assign_permissions_for_role_id"
        logger.info(logs.logJson)
        logger.info(f" PERMISSION ROLE DICTIONARY : {permission_role_dict}")
        try :
            if not created_by: 
                    created_by = "user_dev"
            count = 0 
            self.role_name_list = self.get_role_name_list()
            logger.info(f"ROLE NAME LIST : {self.role_name_list}")
           
            # {'admin': ['CUSR', 'EUSR'], 'operator': ['CUSR', 'VUSR', 'DUSR'], 'executive': ['CUSR', 'VUSR', 'DUSR']}
            # 1. get roles from dictionary
            # 2. get role id from role
            # 3. delete all permissions ids for that role id in association table
            # 4. insert new permissions ids for that role id in association table by insert query
            for role_key,permission_code_list in permission_role_dict.items() :
                for item in self.role_name_list :
                    if item['roleName'] == role_key:
                            print(f" item['roleId'] {item['roleId']}")
                            role_id = item['roleId']
                            print(f"ROLE ID FROM DICT : {role_id}")
                            # delete existing permissions_id mapped with role id in association table if exists
                            
                            delete_query = f"DELETE FROM TMS_admin.adm_role_permission_assoc WHERE role_id ={role_id};"
                            rows_deleted= self.delete_query_execution(delete_query)
                            print(f"{rows_deleted} records associated with role id {role_id} deleted successfully .")
                                
                            # empty list condition
                            # permission_code_list = permission_role_dict[role_key]
                            if not permission_code_list:
                                raise ValueError(f"The list is empty for role id {role_id}")
                            
                            permission_ids = self.get_permission_id_for_code(permission_code_list)
                            # insert new permission associated with role id in mapping table
                            print(f"NEW PERMISSION IDS : {permission_ids}")

                            query =  f"insert into TMS_admin.adm_role_permission_assoc(role_id, permission_id, is_enabled, created_by, created_date, updated_by, updated_date, checked_status, is_deleted) values(%s, %s, true, %s, CURRENT_TIMESTAMP, %s, CURRENT_TIMESTAMP, true, false);"
                            values = []
                            for permission_id in permission_ids:
                                value = (role_id, permission_id, created_by, created_by)
                                values.append(value)
                                print(f"VALUE ADDED TO TUPLE : {value}")
                                
                            self.bulk_insert_role_permission_assoc(query,values)
                            
                    
            return count
               
        except Exception as e :
            print("Exception occurred in assign_permissions_for_role_id():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            print(f"Exception type: {exception_type} ------  Line number:{line_number} ---- File name: {filename}")
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    def delete_query_execution(self,delete_query=None):
        try : 
            print(f"DELETE QUERY : {delete_query}")
            if delete_query:
                self.cursor.execute(delete_query)
                print(f"Records deleted successfully .")
                return self.cursor.rowcount
            else :
                logger.info(f"Delete query is not given as argument")
                
        except Exception as e :
            print("Exception occurred in delete_query_execution():", e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno 
            print(f"Exception type: {exception_type} ------  Line number:{line_number} ---- File name: {filename}")
            logger.info(f"Exception type: {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))

    def bulk_insert_role_permission_assoc(self, query, values):

        try:
            self.cursor.executemany(query, values)
            count = self.cursor.rowcount
            print(f"{count} records inserted successfully.")
            return count
        except Exception as e:
            print(f"Error occurred during bulk insert: {e}")
            return 0

        
    def insert_query_execution(self, query, query_params):
        # logger
        print(f"QUERY  : {query}")
        print(f"QUERY PARAMS : {query_params}")
        logs.logJson['UniqueValue']= str(random.randint(0, 999999))
        logs.logJson['Message']= "Inside insert_query_execution()"
        logs.logJson['Tag']="insert_query_execution"
        logs.logJson['Endpoint']="TMSApp"
        logger.info(logs.logJson)

        # code
        try:
            self.cursor.execute(query, query_params)
            print(f"Query executed: {query}")
            logger.info(f"Query executed >>>")
            if self.cursor.rowcount:
                logger.info(f"Successfully no. of rows inserted: {self.cursor.rowcount}")
            return self.cursor.rowcount
        except Exception as e:
            print("Exception occurred while executing query:", e)
            # Log the exception details if needed
            exception_type, exc_obj, exc_tb = sys.exc_info()
            filename = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
            print(f"File name: {filename}")
            logger.info(f"Exception occurred while executing query: {e}")
            logger.info(f"Exception Type : {exception_type}")
            logger.info(f"File name: {filename}")
            logger.info(f"Line number:{line_number}")
            logger.info(Exception(e))
            return 0
    






# Example usage:
# if __name__ == "__main__":
    # db = TMSDatabaseManager()
    # db.connect()
    # db.get_model_list('','Yamah')
    # db.add_model("TMS","test_create")

    
    ########################################################
    # db = AdminDatabaseManager()
    # db.connect()
    # roles =  json.loads(db.get_role_details())
    # permissions =  json.loads(db.get_permission_list())
    # print(f"printing roles : {roles['data'][0]['roleName']}")
    # print(f"printing roles : {permissions}")

    # output = db.get_permission_id_for_code(["CUSR","DUSR","LRL"])
    # print(f"output : {output}")
    # print("DB CONNECTED :*******************")
    
    # result =  db.get_user_details()
    # print("RESULT : "+ str(result))
    # res = {}
    # final = {"data": [], "status": 0,"message":""}
    # if len(result) != 0:
    #     for index,val in enumerate(result):
    #                     res["userId"] = val[0]
    #                     res["userName"] = val[1]
    #                     res["name"] = val[2] + " " + val[3]
    #                     final["data"].append(res)
    #                     print(res)
    # final["status"] = "200"
    # final["message"]= "Good"
    # print(f"Final json {final}")    
    # print("---------------- START --------------")
                 
    # db.add_user("hpatil","Harshal","Patil","TMS0122","admin@123",2,"test_admin")
    # db.add_user("jlebron","Lebron","James","TMS0123","admin@123",2,"test_admin")
    # db.add_user("kJain","Kishoree","Jain","TMS0124","admin@123",2,"test_admin")
    # db.add_user("sjadhav","Sanket","Jadhav","TMS0125","admin@123",2,"test_admin")
    # db.add_user("sgurav","Sameedha","Gurav","TMS0127","admin@123",2,"test_admin")
    # db.add_user("temarson","tesla","emarson","TMS0128","admin@123",2,"test_admin")
    # db.add_user("shem","shirish","hemal","TMS0129","admin@123",2,"test_admin")
    # db.add_user("rreddy","raj","reddy","TMS0131","admin@123",2,"test_admin")
    # db.add_user("kcr","kiran","rao","TMS0132","admin@123",2,"test_admin")
    # db.add_user("stiwari","Shananu","Tiwari","TMS0133","admin@123",1,"test_admin")

    
    # db.check_login("asharma","admin@123")
    # role_id = 2
    # list_of_permission = [14,18,19]
    # db.assign_permissions_for_role_id(role_id,list_of_permission,"Test_Admin")
    # db.edit_user_details("TMS0127","gsameedha",None,None,"tejas")
    # db.add_new_role("suser" , "super user","dev_team")
    # db.update_permission_details(17,"MODHIS","Model Historical Data")
    # db.update_role_details(8,"executive")

    # print("---------------- END --------------")
        
    # db.get_role_list()
    # db.add_new_role("Senior Operator", "Operator supervisor")
    # db.add_new_permission("Tejas","TEST","1st permission Insert","dev_tej")
    # db.delete_role_with_mappings(7)
    # db.get_role_list()
    # print(f"ACTION DETAILS :{db.add_defect()}")

    # db.disconnect()
