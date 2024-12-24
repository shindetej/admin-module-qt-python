import bcrypt


class AuthorizationUtils:

    @staticmethod
    def generate_hashed_password(password):
        try:
            print(f"generated _hashed passwored method")

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            return hashed_password
        except Exception as e:
            print(f"Error hashing password: {e}")
            return None
        
    @staticmethod
    def verify_password(entered_password,hashed_password):
        print("In verify_password()")
        try :
            entered_password_encoded =  entered_password.encode('utf-8')
            bytes_of_hashed_password = bytes(hashed_password)
            if bcrypt.checkpw(entered_password_encoded,bytes_of_hashed_password): 
                return True
            else:
                return False
        except Exception as e :     
            print(f"Error verifying password: {e}")
            return False

        


