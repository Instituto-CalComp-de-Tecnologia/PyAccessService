from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from service.access_service import AccessService
from service.user_service import UserService
from service.pessoas_adicionais_service import PessoasAdicionaisService
from service.departamento_service import DepartamentoService
from service.lines_service import LinesService
import json

# LEITURA DAS CONFIGURAÇÕES
with open("src/config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    jsonfile.close()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

access_service = AccessService(config)
user_service = UserService(config)
pessoas_service = PessoasAdicionaisService(config)
departamento_service = DepartamentoService(config)
lines_service = LinesService(config)

# ROTAS ACCESS ------------------------------------------------------------------------------
@app.route("/getaccess/<local>", methods=['GET'])
@cross_origin()
def find_total_acess_today_detail(local: str):
    try:
        data = access_service.find_total_acess_today_detail(local=local)
        return {
            'status': True,
            'message': 'Access successfully listed',
            'data': data
        }
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on list access: ' + str(err),
            'data': []
        }

@app.route("/getaccesstoday/", methods=['GET'])
@cross_origin()
def get_total_access_by_local_today():
    try:
        data = access_service.get_total_access_by_local_today()
        return {
            'status': True,
            'message': 'Access successfully listed',
            'data': data
        }
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on list access: ' + str(err),
            'data': []
        }

@app.route("/getpresents/<local>", methods=['GET'])
@cross_origin()
def get_present_people_by_local(local: str):
    try:
        data = access_service.get_present_people_by_local(local=local)
        return {
            'status': True,
            'message': 'Access successfully listed',
            'data': data
        }
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on list access: ' + str(err),
            'data': []
        }
# -----------------------------------------------------------------------------------------

# ROTAS USER ------------------------------------------------------------------------------
@app.route("/user/login", methods=['POST'])
@cross_origin()
def login_user():
    try:
        password = request.json["password"]
        data = user_service.login(password=password)
        return data
    except Exception as err:
        return {
            'status': False,
            'message': 'Error login user: ' + str(err),
            'data': []
        }

@app.route("/user/create", methods=['POST'])
@cross_origin()
def create_user():
    try:
        userName = request.json["userName"]
        password = request.json["password"]
        data = user_service.create(userName=userName, password=password)
        return data
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on create user: ' + str(err),
            'data': []
        }
# --------------------------------------------------------------------------------------------------------

# ROTAS PESSOAS_ADICIONAIS  ------------------------------------------------------------------------------
@app.route("/pessoas/getall", methods=['GET'])
@cross_origin()
def pessoas_get_all():
    try:
        data = pessoas_service.get_all()
        return {
            'status': True,
            'message': 'Pessoas successfully listed.',
            'data': data
        }
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on list pessoas: ' + str(err),
            'data': []
        }

@app.route("/pessoas/update", methods=['POST'])
@cross_origin()
def pessoas_update():
    try:
        pessoa_id = request.json["pessoa_id"]
        id_departamento = request.json["id_departamento"]
        id_line = request.json["id_line"]
        
        data = pessoas_service.update_pessoa(pessoa_id=pessoa_id, id_departamento=id_departamento, id_line=id_line)
        return {
            'status': True,
            'message': 'Pessoas successfully updated.',
            'data': []
        }
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on list pessoas: ' + str(err),
            'data': []
        }
# -------------------------------------------------------------------------------------------------------

# ROTAS DEPARTAMENTOS  ------------------------------------------------------------------------------
@app.route("/departamento/getall", methods=['GET'])
@cross_origin()
def departamento_get_all():
    try:
        data = departamento_service.get_all()
        return {
            'status': True,
            'message': 'Departamento successfully listed.',
            'data': data
        }
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on list departamento: ' + str(err),
            'data': []
        }
# -------------------------------------------------------------------------------------------------------

# ROTAS LINES  ------------------------------------------------------------------------------
@app.route("/lines/getall", methods=['GET'])
@cross_origin()
def lines_get_all():
    try:
        data = lines_service.get_all()
        return {
            'status': True,
            'message': 'Lines successfully listed.',
            'data': data
        }
    except Exception as err:
        return {
            'status': False,
            'message': 'Error on list Lines: ' + str(err),
            'data': []
        }
# -------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)