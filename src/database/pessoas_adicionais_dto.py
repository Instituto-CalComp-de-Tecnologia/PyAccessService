import pyodbc

class PessoasAdicionaisDTO:
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
                               SELECT p.id,
                                      p.n_folha,
                                      p.nome,
                                      (l.desc_line) line,
                                      (f.descricao) AS departamento
                                FROM pessoas p
                                LEFT JOIN pessoas_adicionais pa
                                    ON p.id = pa.pessoa_id
                                LEFT JOIN lines l
                                    ON l.id = pa.line
                                INNER JOIN filtro2 f
                                    ON P.filtro2_id = f.id
                                ORDER BY p.nome;
                               ''').fetchall()
            cur.close()
            del cur
            con.close()
            return rows
        except Exception as err:
            print(f"Error on login user: {err}")
    
    def update_departamento(self, pessoa_id, id_departamento):
        con = self.connection()
        cur = con.cursor()
        
        try:
            cur.execute(f'''
                        UPDATE pessoas
                        SET filtro2_id = {id_departamento}
                        WHERE id = {pessoa_id};
                        ''')
            con.commit()
            
            cur.close()
            del cur
            con.close()
            return {
                'status': True,
                'message': 'Departamento successfully updated.',
                'data': []
            }
        except Exception as err:
            print(f"Error on insert user: {err}")
            cur.close()
            del cur
            con.close()
            return {
                'status': False,
                'message': f'Error on update departamento: {str(err)}',
                'data': []
            }
    
    def update_line(self, pessoa_id, id_line):
        p = self.find_by_id(pessoa_id=pessoa_id)
        con = self.connection()
        cur = con.cursor()
        
        if(len(p) > 0):
            try:
                cur.execute(f'''
                            UPDATE pessoas_adicionais
                            SET line = {id_line}
                            WHERE pessoa_id = {pessoa_id};
                            ''')
                con.commit()
                
                cur.close()
                del cur
                con.close()
                return {
                    'status': True,
                    'message': 'Line successfully updated.',
                    'data': []
                }
            except Exception as err:
                print(f"Error on insert user: {err}")
                cur.close()
                del cur
                con.close()
                return {
                    'status': False,
                    'message': f'Error on update line: {str(err)}',
                    'data': []
                }
        else:
            try:
                cur.execute(f'''
                            INSERT INTO pessoas_adicionais(pessoa_id, line)
                            VALUES({pessoa_id}, {id_line});
                            ''')
                con.commit()
                
                cur.close()
                del cur
                con.close()
                return {
                    'status': True,
                    'message': 'Line successfully updated.',
                    'data': []
                }
            except Exception as err:
                print(f"Error on insert user: {err}")
                cur.close()
                del cur
                con.close()
                return {
                    'status': False,
                    'message': f'Error on update line: {str(err)}',
                    'data': []
                }
    
    def find_by_id(self, pessoa_id):
        con = self.connection()
        cur = con.cursor()
        
        try:
            rows = cur.execute(f'''
                        SELECT pessoa_id
                        FROM pessoas_adicionais
                        WHERE pessoa_id = {pessoa_id};
                           ''').fetchall()
            
            
            cur.close()
            del cur
            con.close()
            return rows
        except Exception as err:
            print(f"Error on find Pessoa adicional: {err}")
            cur.close()
            del cur
            con.close()
            return []

if __name__ == '__main__':
    config = {
        "server": "10.58.65.21",
        "database": "SecullumAcesso",
        "username": "sa",
        "password": "totalseg_1"
    }
    p = PessoasAdicionaisDTO(config=config)
    print(p.update_line(1614, 2))