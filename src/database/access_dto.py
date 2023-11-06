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
                                    f.descricao,
                                    l.desc_line
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
                            LEFT JOIN pessoas_adicionais pa
                                ON p.id = pa.pessoa_id
                            LEFT JOIN lines l
                                ON l.id = pa.line
                            WHERE a.data = FORMAT(GETDATE(), 'yyyy-MM-dd')
                            AND b.descricao = '{local}'
                            AND a.confirmado = 1
                            AND a.negado = 0
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
                                    f.descricao,
                                    l.desc_line
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
                            LEFT JOIN pessoas_adicionais pa
                                ON p.id = pa.pessoa_id
                            LEFT JOIN lines l
                                ON l.id = pa.line
                            WHERE foo.descricao = '{local}'
                            ORDER BY p.nome;
                    ''').fetchall()
        cur.close()
        del cur
        con.close()
        return rows
    
    def get_absents(self, id_departamento, id_line):
        con = self.connection()
        cur = con.cursor()
        where = ''
        
        if((id_departamento != None) and (id_line != None)):
            where = f'''WHERE f.id = {id_departamento}
                          AND l.id = {id_line}'''
        elif((id_departamento != None) and (id_line == None)):
            where = f'''WHERE f.id = {id_departamento}'''
        elif((id_departamento == None) and (id_line != None)):
            where = f'''WHERE l.id = {id_line}'''
            
        rows = cur.execute(f''' 
                            SELECT p.id,
                                    p.n_folha,
                                    p.nome,
                                    (l.id) AS id_line,
                                    (l.desc_line) line,
                                    (f.id) AS id_departamento,
                                    (f.descricao) AS departamento,
                                    (SELECT top 1
                                            dbo.fn_hora_segundos(ea.hora)
                                    FROM eventos_acessos ea
                                    WHERE ea.tipo_acesso = 1
                                    AND ea.confirmado = 1
                                    AND ea.data = FORMAT(GETDATE(), 'yyyy-MM-dd')
                                    AND ea.pessoa_id = p.id
                                    ORDER BY ea.hora) as hor_entrada,
                                    (CASE WHEN f3.descricao IS NULL
									THEN ''
									ELSE f3.descricao END) as desc_turno
                            FROM pessoas p
                            LEFT JOIN pessoas_adicionais pa
                                ON p.id = pa.pessoa_id
                            LEFT JOIN lines l
                                ON l.id = pa.line
                            INNER JOIN filtro2 f
                                ON P.filtro2_id = f.id
                            LEFT JOIN filtro3 f3
                                ON p.filtro3_id = f3.id
                            {where}
                            ORDER BY p.nome;
                    ''').fetchall()
        cur.close()
        del cur
        con.close()
        return rows
    
    def get_entrances_by_date(self, id_pessoa, type_period, init_date, end_date):
        if(type_period == "W"):
            con = self.connection()
            cur = con.cursor()
            rows = cur.execute(f''' 
                               SELECT (CASE
                                        WHEN DATEPART(WEEKDAY, foo.date_compare) = 1 THEN 'Sun'
                                        WHEN DATEPART(WEEKDAY, foo.date_compare) = 2 THEN 'Mon'
                                        WHEN DATEPART(WEEKDAY, foo.date_compare) = 3 THEN 'Tue'
                                        WHEN DATEPART(WEEKDAY, foo.date_compare) = 4 THEN 'Wed'
                                        WHEN DATEPART(WEEKDAY, foo.date_compare) = 5 THEN 'Thu'
                                        WHEN DATEPART(WEEKDAY, foo.date_compare) = 6 THEN 'Fri'
                                        WHEN DATEPART(WEEKDAY, foo.date_compare) = 7 THEN 'Sat'
                                       END) AS week_day,
                                       foo.date_compare,
                                      (SELECT TOP 1 dbo.fn_hora_segundos(ea.hora)
                                       FROM eventos_acessos ea
                                       WHERE ea.tipo_acesso = 1
                                         AND ea.confirmado = 1
                                         AND ea.pessoa_id = {id_pessoa}
                                         AND ea.data = foo.date_compare
                                       ORDER BY ea.hora) as hor_access
                                FROM(
                                    SELECT DATEADD(DAY,value, FORMAT(GETDATE(), 'yyyy-MM-dd 00:00:00.000')) AS date_compare
                                    FROM dbo.GENERATE_SERIES(0, -6, -1)) AS foo
                                WHERE DATEPART(WEEKDAY, foo.date_compare) NOT IN(1, 7)
                                ORDER BY foo.date_compare DESC;
                        ''').fetchall()
            cur.close()
            del cur
            con.close()
            return rows
            
        if(type_period == "P"):
            con = self.connection()
            cur = con.cursor()
            rows = cur.execute(f''' 
                                SELECT(CASE
                                        WHEN DATEPART(WEEKDAY, foo2.date_compare) = 1 THEN 'Sun'
                                        WHEN DATEPART(WEEKDAY, foo2.date_compare) = 2 THEN 'Mon'
                                        WHEN DATEPART(WEEKDAY, foo2.date_compare) = 3 THEN 'Tue'
                                        WHEN DATEPART(WEEKDAY, foo2.date_compare) = 4 THEN 'Wed'
                                        WHEN DATEPART(WEEKDAY, foo2.date_compare) = 5 THEN 'Thu'
                                        WHEN DATEPART(WEEKDAY, foo2.date_compare) = 6 THEN 'Fri'
                                        WHEN DATEPART(WEEKDAY, foo2.date_compare) = 7 THEN 'Sat'
                                        END) AS week_day,
                                        foo2.date_compare,
                                    (SELECT TOP 1 dbo.fn_hora_segundos(ea.hora)
                                    FROM eventos_acessos ea
                                    WHERE ea.tipo_acesso = 1
                                        AND ea.confirmado = 1
                                        AND ea.pessoa_id = {id_pessoa}
                                        AND ea.data = foo2.date_compare
                                    ORDER BY ea.hora) as hor_access
                                FROM(
                                SELECT DATEADD(DAY, foo.value, '{init_date}') AS date_compare
                                FROM(
                                    SELECT value
                                    FROM dbo.GENERATE_SERIES(1, 300, 1)) AS foo
                                WHERE foo.value <= DATEDIFF(DAY, '{init_date}', '{end_date}')) AS foo2
                                WHERE DATEPART(WEEKDAY, foo2.date_compare) NOT IN(1, 7)
                                ORDER BY foo2.date_compare DESC;
                        ''').fetchall()
            cur.close()
            del cur
            con.close()
            return rows
    
    def get_refectory_access_by_date(self, init_date, final_date, shift, service: str):
        # list_turnos = ', '.join(str(turno) for turno in shift)
        
        #CAFÉ DA MANHÃ
        if(service.lower() == 'b'):
            where = 'AND (a.hora >= 19800 AND a.hora <= 32400)'
        
        #CAFÉ DA MANHÃ - GESTANTES
        if(service.lower() == 'p'):
            where = 'AND ((a.hora >= 34200 AND a.hora <= 3600) OR (a.hora >= 55800 AND a.hora <= 57600))'
        
        #ALMOÇO
        if(service.lower() == 'l'):
            where = 'AND (a.hora >= 39600 AND a.hora <= 50400)'
        
        #JANTA
        if(service.lower() == 'd'):
            where = 'AND (a.hora >= 72000 AND a.hora <= 79200)'
        
        #CEIA
        if(service.lower() == 's'):
            where = 'AND (a.hora >= 3600 AND a.hora <= 5400)'
        
        #LANCHE
        if(service.lower() == 'sn'):
            where = 'AND ((a.hora >= 59400 AND a.hora <= 64800) OR (a.hora >= 81000 AND a.hora <= 86399) OR (a.hora >= 10800 AND a.hora <= 1200))'
        
        con = self.connection()
        cur = con.cursor()
        rows = cur.execute(f''' 
                            SELECT  p.id as id_pessoa,
                                    p.n_folha,
                                    p.nome,
                                    c.descricao AS classificacao,
                                    f.descricao AS departamento,
                                    f3.descricao AS turno,
                                    l.desc_line,
                                    count(p.id) as qtd_acessos
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
                            LEFT JOIN filtro3 f3
                                ON p.filtro3_id = f3.id
                            LEFT JOIN pessoas_adicionais pa
                                ON p.id = pa.pessoa_id
                            LEFT JOIN lines l
                                ON l.id = pa.line
                            WHERE (a.data >= FORMAT(convert(DATETIME, '{init_date}'), 'yyyy-MM-dd') AND a.data <= FORMAT(convert(DATETIME, '{final_date}'), 'yyyy-MM-dd'))
                            AND b.descricao = 'REFECTORY'
                            AND a.confirmado = 1
                            AND a.negado = 0
                            AND a.tipo_acesso = 1
                            AND p.filtro3_id = ({shift})
                             {where}
                            GROUP BY p.id, p.n_folha, p.nome, c.descricao, f.descricao, f3.descricao, l.desc_line
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
    config = {
        "server": "10.58.65.21",
        "database": "SecullumAcesso",
        "username": "sa",
        "password": "totalseg_1"
    }
    s = AccessDTO(config=config)
    s.get_refectory_access_by_date(init_date='10/24/2023', final_date='10/24/2023', shift=1, service='P')