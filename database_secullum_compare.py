import datetime
import hashlib
import requests
import pyodbc
import json

server = '10.58.65.21'
database = 'SecullumHomolog'
username = 'sa'
password = 'totalseg_1'

con = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

def find_turno_by_desc(desc: str):
    cur = con.cursor()
    row = cur.execute(f'''
                       SELECT id
                       FROM filtro3
                       WHERE descricao = '{desc}'
                    ''').fetchone()
    cur.close()
    return row.id

def find_func_secullum():
    cur = con.cursor()
    rows = cur.execute(f'''
                        select n_folha,
                            nome
                        from pessoas
                        where classificacao_id = 2
                        and estado = 2
                        order by nome;
                    ''').fetchall()
    cur.close()
    return rows

date = datetime.datetime.now()
date = date.strftime("%Y%m%d")
token_str = f"ACCESS-FACEID-{date}"
token = hashlib.sha256(token_str.encode()).hexdigest()
headers = {'token': token}
print(f"Token: {token}")

url = 'http://10.58.64.202:7932/CalcompDataEmployees/all'

try:
    response = requests.get(url, headers=headers)
    data = response.json()
except Exception as err:
    print(f"Error on request employees: {err}")
    
data_totvs = []
for func in data:
    dat = {
        'registration': func['rA_CRACHA'],
        'name': func['name']
    }
    data_totvs.append(dat)
 
with open('result_totvs.json', 'w') as fp:
    json.dump(data_totvs, fp)    
    
data_secullum = []
for fun in find_func_secullum():
    dat_sec = {
        'registration': fun.n_folha,
        'name': fun.nome
    }
    data_secullum.append(dat_sec)

with open('result_secullum.json', 'w') as fp:
    json.dump(data_secullum, fp)