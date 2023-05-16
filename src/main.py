from flask import Flask
from flask_cors import CORS, cross_origin
from service.access_service import AccessService

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
access_service = AccessService()

@app.route("/getaccess/<local>", methods=['GET'])
@cross_origin()
def hefind_total_acess_today_detail(local: str):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)