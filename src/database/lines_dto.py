import pyodbc

class LinesDTO:
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
    
    def get_all(self):
        con = self.connection()
        cur = con.cursor()
        
        try:
            rows = cur.execute(f'''
                               SELECT id,
                                      desc_line
                               FROM lines
                               ORDER BY id;
                               ''').fetchall()
            cur.close()
            del cur
            con.close()
            return rows
        except Exception as err:
            print(f"Error on login user: {err}")

if __name__ == '__main__':
    config = {
        "server": "10.58.65.21",
        "database": "SecullumAcesso",
        "username": "sa",
        "password": "totalseg_1"
    }
    p = LinesDTO(config=config)
    print(p.get_all())