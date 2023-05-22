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

EMPRESAS = {
    '21.640.591/0001-31': 1,
    '07.200.194/0003-80': 2,
    '07.200.194/0001-18': 3,
    '21.315.035/0001-90': 4
}

CLASSIFICACAO = 2

server = '10.58.65.21'
database = 'SecullumAcesso'
username = 'sa'
password = 'totalseg_1'

con = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

url = 'http://10.58.64.202:7932/CalcompDataEmployees/Secullum-Export-txt/file'

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

text = response.text
length = len(text.split('\n'))

# INSERÇÃO DOS NOVOS COLABORADORES NA BASE DE DADOS -------------------------------------------------------------------------------
for i, data in enumerate(text.split('\n')):
    if((i == 0) or (i == (length - 1))):
        continue
    n_identificador = data.split('\t')[0]
    nome = data.split('\t')[1]
    cnpj = data.split('\t')[2]
    classificacao = data.split('\t')[3]
    
    cur = con.cursor()
    cur.execute(f"SELECT pessoas.id, pessoas.nome FROM pessoas WHERE pessoas.n_identificador = '{n_identificador}'")
    row = cur.fetchmany()
    cur.close()
    if(len(row) < 1):
        # cur = con.cursor()
        # cur.execute(f"INSERT INTO pessoas(n_identificador, nome, empresa_id, horario_id, estado, classificacao_id, nivel_id, sem_digital, criacao_usu_id, criacao_data) VALUES('{n_identificador}', '{nome}', {EMPRESAS[cnpj]}, 1, 2, 2, 1, 0, 2, GETDATE())")
        # con.commit()
        # cur.close()
        print(f"INSERIDO: {n_identificador} - {nome} - {cnpj} ({EMPRESAS[cnpj]}) - {classificacao}")
# --------------------------------------------------- -------------------------------------------------------------------------------

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
    cur.execute(f"SELECT pessoas.id, pessoas.nome FROM pessoas WHERE pessoas.n_identificador = '{rA_MAT}' AND n_folha IS NULL")
    row = cur.fetchmany()
    cur.close()
    # if(len(row) > 0):
    #     pessoa_id = row[0].id
    #     cur = con.cursor()
    #     cur.execute(f'''
    #                 UPDATE pessoas
    #                 SET n_folha = '{rA_CRACHA}'
    #                 WHERE id = {pessoa_id}
    #                 ''')
    #     con.commit()
    #     cur.close()
    #     print(f"Atualizado: {rA_CRACHA} - {row[0].nome}")
# --------------------------------------------------- -------------------------------------------------------------------------------