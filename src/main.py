from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from service.access_service import AccessService
from service.user_service import UserService
from service.pessoas_adicionais_service import PessoasAdicionaisService
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
            'message': 'Error on list access: ' + err,
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
            'message': 'Error on list access: ' + err,
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
            'message': 'Error on list access: ' + err,
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
            'message': 'Error login user: ' + err,
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
            'message': 'Error on create user: ' + err,
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
            'message': 'Error on create user: ' + err,
            'data': []
        }
# -------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)