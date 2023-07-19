import pyodbc

class AccessDTO:
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
    
    def get_access_today_detail(self, local: str):
        '''
            Retorna todos os acessos na data de hoje  conforme parâmetros type_access:
            1 = Entradas
            2 = Saídas
            
            e local: ['LENOVO', 'NEWLAND', 'RECEPCAO', 'SMT', 'SSD', 'WAREHOUSE']
        '''
        con = self.connection()
        cur = con.cursor()
        rows = cur.execute(f'''
                    SELECT a.id,
                           a.data,
                           dbo.fn_hora_segundos(a.hora) hora,
                           p.n_folha,
                           p.nome,
                           CASE a.tipo_acesso
                            WHEN 0 THEN 'R'
                            WHEN 1 THEN 'E'
                            WHEN 2 THEN 'S'
                           END AS tipo_acessos,
                           e.descricao,
                           b.descricao,
                           c.descricao,
                           f.descricao
                    FROM eventos_acessos a
                    INNER JOIN pessoas p
                        ON a.pessoa_id = p.id
                        INNER JOIN classificacoes c
	                        ON p.classificacao_id = c.id
                    INNER JOIN equipamentos e
                        ON a.equipamento_id = e.id
                    LEFT JOIN ambientes b
                        ON e.ambiente_id = b.id
                    LEFT JOIN filtro2 f
                        ON p.filtro2_id = f.id
                    WHERE a.data = FORMAT(GETDATE(), 'yyyy-MM-dd')
                    AND b.descricao = '{local}'
                    AND a.confirmado = 1
                    ORDER BY a.hora DESC;
                    ''').fetchall()
        cur.close()
        del cur
        con.close()
        return rows
    
    def get_total_access_by_local_today(self):
        data_return = {}
        locs = self.get_locals()
        classifications = self.get_classifications()
        
        con = self.connection()
        cur = con.cursor()
        rows = cur.execute(f''' 
                        SELECT a.id,
                            CASE a.tipo_acesso
                                WHEN 0 THEN 'R'
                                WHEN 1 THEN 'E'
                                WHEN 2 THEN 'S'
                            END AS tipo_acessos,
                            e.descricao,
                            b.descricao,
                            c.descricao
                        FROM eventos_acessos a
                        INNER JOIN pessoas p
                            ON a.pessoa_id = p.id
                        INNER JOIN classificacoes c
                            ON p.classificacao_id = c.id
                        INNER JOIN equipamentos e
                            ON a.equipamento_id = e.id
                        LEFT JOIN ambientes b
                            ON e.ambiente_id = b.id
                        WHERE a.data = FORMAT(GETDATE(), 'yyyy-MM-dd')
                        AND a.confirmado = 1
                        ORDER BY a.hora DESC;
                    ''').fetchall()
        cur.close()
        del cur
        con.close()
        
        for id, local in locs:
            data_return[local] = {}
            
        for local in data_return:
            for id, classification in classifications:
                data_return[local][classification] = 0
        
        for row in rows:
            if(row[1] == 'E'):
                data_return[row[3]][row[4]] += 1
            if(row[1] == 'S'):
                data_return[row[3]][row[4]] -= 1
        return data_return
    
    def get_present_people_by_local(self, local):
        '''
            RETORNA AS PESSOAS QUE ESTAO PRESENTES POR LOCAL (BEM COMO TOTAL)
        '''
        con = self.connection()
        cur = con.cursor()
        rows = cur.execute(f'''  
                    SELECT p.id,
                           p.n_folha,
                           p.nome,
                           c.descricao,
                           foo.descricao,
                           f.descricao
                    FROM pessoas p
                    INNER JOIN (
                                SELECT ea.pessoa_id,
				                       a.descricao,
				                       MAX(ea.hora) AS hora
			                    FROM eventos_acessos ea
			                    INNER JOIN equipamentos e
				                    ON ea.equipamento_id = e.id
			                    INNER JOIN ambientes a
				                    ON e.ambiente_id = a.id
			                    WHERE ea.data = FORMAT(GETDATE(), 'yyyy-MM-dd')
                                  AND ea.confirmado = 1
			                      AND ea.tipo_acesso = 1
			                      AND NOT EXISTS (SELECT ea2.pessoa_id
							                      FROM eventos_acessos ea2
							                      WHERE ea2.pessoa_id = ea.pessoa_id
								                    AND ea2.confirmado = 1
								                    AND ea2.tipo_acesso = 2
								                    AND ea2.data = FORMAT(GETDATE(), 'yyyy-MM-dd')
								                    AND ea2.hora > ea.hora)
			                    GROUP BY ea.pessoa_id, a.descricao) AS foo
                        ON p.id = foo.pessoa_id
                    INNER JOIN classificacoes c
                        ON c.id = p.classificacao_id
                    LEFT JOIN filtro2 f
                        ON p.filtro2_id = f.id
                    WHERE foo.descricao = '{local}'
                    ORDER BY p.nome;
                    ''').fetchall()
        cur.close()
        del cur
        con.close()
        return rows
    
    def get_locals(self):
        con = self.connection()
        cur = con.cursor()
        rows = cur.execute(f''' 
                        SELECT id,
                               descricao
                        FROM ambientes
                    ''').fetchall()
        cur.close()
        del cur
        con.close()
        return rows
    
    def get_classifications(self):
        con = self.connection()
        cur = con.cursor()
        rows = cur.execute(f'''
                        SELECT id,
                               descricao
                        FROM classificacoes
                    ''').fetchall()
        cur.close()
        del cur
        con.close()
        return rows

if __name__ == '__main__':
    s = AccessDTO()
    # s.get_access_today('RECEPCAO')
    s.get_total_access_by_local_today()