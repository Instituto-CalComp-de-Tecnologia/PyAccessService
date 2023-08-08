import datetime
import hashlib
import requests
import pyodbc

server = '10.58.65.21'
database = 'SecullumAcesso'
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

def find_func_by_register(register: str):
    cur = con.cursor()
    row = cur.execute(f'''
                       SELECT id
                       FROM pessoas
                       WHERE n_folha = '{register}';
                    ''').fetchone()
    cur.close()
    if(not row == None):
        return row.id
    else:
        return None

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
    
turnos = []

for func in data:
    func_id = find_func_by_register(func['rA_XMATRCC'])
    if(not func_id == None):
        try:
            turno_id = find_turno_by_desc(func['desC_TURNO'])
            cur = con.cursor()
            cur.execute(f'''
                        UPDATE pessoas
                        SET filtro3_id = {turno_id}
                        WHERE id = {func_id};
                ''')
            con.commit()
            cur.close()
            print(f"UPDATE: {func['rA_XMATRCC']} - id: {func_id} - Turno: {turno_id}")
        except Exception as err:
            print(f'Erro ao realizar update: {err}')
    
#     if(func['desC_TURNO'] not in turnos):
#         turnos.append(func['desC_TURNO'])

# for turno in turnos:
#     id_turno = find_turno_by_desc(turno)
#     print(f"{turno} - id: {id_turno}")