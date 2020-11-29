import os
from google.cloud import firestore
from google.cloud.firestore_v1 import Client
import uuid
import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ml.json'


class User(object):
    def __init__(self, user, password, name):
        self.user = user
        self.password = password
        self.name = name

    def to_dict(self):
        obj_dict = {
            "name": self.name,
            "user": self.user,
            "password": self.password,
            "registration_date": datetime.datetime.now()
        }
        return obj_dict

    @staticmethod
    def from_dict(obj_json):
        user = User(obj_json["user"], obj_json["password"], obj_json["name"])
        return user


def insert_user(obj_json: dict, collection: str):
    try:
        db = get_client()
        doc_ref = db.collection(collection)
        doc_ref.document(str(uuid.uuid4())) \
            .set(User(obj_json["user"], obj_json["password"], obj_json["name"]).to_dict())
        res_status = {
            "status": True,
            "msj": "Success"
        }
        return res_status
    except Exception as e:
        res_status = {
            "status": False,
            "msj": f"Failed: {e.__class__}"
        }
        return res_status


def get_client() -> Client:
    db = firestore.Client()
    return db


def find_user(obj_json: dict, collection: str):
    try:
        db = get_client()
        users_ref = db.collection(collection)
        query_ref = users_ref.where(u'user', u'==', obj_json["user"])\
            .where(u'password', u'==', obj_json["password"]).get()
        size = len(query_ref)
        if size > 0:
            obj_res = {
                "status": True,
                "value": query_ref[0].to_dict()
            }
            return obj_res
        else:
            obj_res = {
                "status": False,
                "value": "Error: Not Found"
            }
            return obj_res
    except Exception as e:
        obj_res = {
            "status": False,
            "value": f"Error: {e.__class__}"
        }
        return obj_res
