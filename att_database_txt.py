'''
    SCRIPT PARA ATUALIZAÇÃO DA BASE DE DADOS DO CONTROLE DE ACESSO DAS CATRACAS,
    O SCRIPT PEGA A LISTA DE PESSOAS DA API 'http://10.58.64.202:7932/CalcompDataEmployees/Secullum-Export-txt/file'
    DESSA LISTA QUE VEM DA API, VERIFICA QUEM NÃO ESTÁ NA BASE DE DADOS DA CATRACA. QUEM NÃO ESTIVER, É INSERIDO.
    
    PARA FAZER REQUISIÇÃO DA API É NECESSÁRIO TER NO HEADER A SEGUINTE STRING CONVERTIDA EM SHA256: 'ACCESS-FACEID-yyyyMMdd'
'''

import requests
import datetime
import hashlib
import pyodbc

server = '10.58.65.21'
database = 'SecullumAcesso'
username = 'sa'
password = 'totalseg_1'

con = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# ATUAIZAÇÃO DE DEMAIS DADOS --------------------------------------------------------------------------------------------------------
url = 'http://10.58.64.202:7932/CalcompDataEmployees/all'

date = datetime.datetime.now()
date = date.strftime("%Y%m%d")
token_str = f"ACCESS-FACEID-{date}"
token = hashlib.sha256(token_str.encode()).hexdigest()
print(f"Token: {token}")

headers = {'token': token}

try:
    response = requests.get(url, headers=headers)
except Exception as err:
    print(f"Error on request employees: {err}")

data = response.json()

for func in data:
    rA_CRACHA = func['rA_CRACHA']
    rA_MAT = func['rA_MAT']
    cur = con.cursor()
    cur.execute(f"SELECT pessoas.id, pessoas.nome, pessoas.n_folha FROM pessoas WHERE pessoas.n_identificador = '{rA_MAT}' AND (pessoas.n_folha IS NULL OR pessoas.n_folha = '')")
    row = cur.fetchmany()
    cur.close()
    if(len(row) > 0):
        try:
            pessoa_id = row[0].id
            cur = con.cursor()
            cur.execute(f'''
                        UPDATE pessoas
                           SET n_folha = '{rA_CRACHA}'
                         WHERE id = {pessoa_id}
                        ''')
            con.commit()
            cur.close()
            print(f"Atualizado: {rA_CRACHA} - {row[0].nome}")
        except Exception as err:
            print(f"Erro ao atualizar funcionário: {str(err)}")
# --------------------------------------------------- -------------------------------------------------------------------------------