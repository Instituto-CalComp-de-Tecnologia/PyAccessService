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
    if(len(row) > 0):
        print(f"Encontrado: {row[0].id} - {row[0].nome}")