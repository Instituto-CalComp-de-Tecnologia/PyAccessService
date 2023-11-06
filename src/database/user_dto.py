import pyodbc
import hashlib

class UserDTO:
    def __init__(self, config) -> None:
        self.server = config["server"]
        self.database = config["database"]
        self.username = config["username"]
        self.password = config["password"]
    
    def connection(self):
        try:
            con = pyodbc.connect('DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password + ";MARS_Connection=yes;MultipleActiveResultSets=True;")
            return con
        except Exception as err:
            con = None
            print(f"Erro ao tentar acessar o SQL Server: {err}")
            return con
    
    def generateMD5(self, password: str):
        md5Password = hashlib.md5(password.encode())
        return md5Password.hexdigest()
    
    def create(self, userName: str, password: str):
        con = self.connection()
        cur = con.cursor()
        hashPassword = self.generateMD5(password=password)
        
        try:
            cur.execute(f'''
                           INSERT INTO dashboard_user(user_name, password) VALUES('{userName}', '{hashPassword}');
                           ''')
            con.commit()
            
            cur.close()
            del cur
            con.close()
            print(f"Usuário inserido com sucesso!")
            return {
                'status': True,
                'message': 'User successfully created.',
                'data': []
            }
        except Exception as err:
            print(f"Error on insert user: {err}")
            cur.close()
            del cur
            con.close()
            return {
                'status': False,
                'message': f'Error on create user: {str(err)}',
                'data': []
            }
    
    def login(self, password: str):
        hashPassword = self.generateMD5(password=password)
        con = self.connection()
        cur = con.cursor()
        
        try:
            rows = cur.execute(f'''
                               SELECT * FROM dashboard_user WHERE password = '{hashPassword}';
                               ''').fetchall()
            cur.close()
            del cur
            con.close()
            if(len(rows) > 0):
                if("refeitorio" in rows[0].user_name):
                    return {
                        'status': True,
                        'UserRefectory': True
                    }
                else:
                    return {
                        'status': True,
                        'UserRefectory': False
                    }
            else:
                return {
                        'status': False,
                        'UserRefectory': False
                    }
        except Exception as err:
            print(f"Error on login user: {err}")

if __name__ == '__main__':
    config = {
        "server": "10.58.65.21",
        "database": "SecullumAcesso",
        "username": "sa",
        "password": "totalseg_1"
    }
    
    u = UserDTO(config=config)
    
    print(u.login(password='Refeitorio@1'))