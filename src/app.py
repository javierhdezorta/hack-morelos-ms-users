import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
import firestore_handler


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)

collection = 'users'


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    get_json = request.json
    if 'user' in get_json and 'password' in get_json :
        if str(get_json['user']).strip() != '' and str(get_json['password']).strip() != '':
            get_status = firestore_handler.find_user(get_json, collection)
            if not get_status["status"]:
                res_status = {
                    "status": False,
                    "msj": "User does not exist"
                }
                return res_status
            else:
                res_status = {
                    "status": True,
                    "msj": "User exists"
                }
                return res_status
        else:
            abort(404, description="User or Password or Name")
            return None
    else:
        abort(404, description="User or Password or Name")
        return None


@app.route('/api/insert', methods=['POST'])
@cross_origin()
def insert():
    get_json = request.json
    if 'user' in get_json and 'password' in get_json and 'name' in get_json:
        if str(get_json['user']).strip() != '' and str(get_json['password']).strip() != '' and str(get_json['name']).strip() != '':
            get_status = firestore_handler.find_user(get_json, collection)
            if not get_status["status"]:
                insert_status = firestore_handler.insert_user(get_json,collection)
                return insert_status
            else:
                res_status = {
                    "status": False,
                    "msj": "User exists"
                }
                return res_status
        else:
            abort(404, description="User or Password or Name")
            return None
    else:
        abort(404, description="User or Password or Name")
        return None


@app.route("/api")
@cross_origin()
def home():
    return jsonify({"api_status": "Success"})


app.run()
