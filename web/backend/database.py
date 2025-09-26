import os, sys
import datetime
from .utilities import *
from .variables import *

from flask import request
import firebase_admin
from google.cloud.firestore import FieldFilter
from firebase_admin import credentials, firestore
from google.oauth2 import service_account
from google.cloud import secretmanager


firebase_client = None
firebase_db = None
firestore_client = None
firestore_db = None

def secrets_init():
    os.makedirs("secure", exist_ok=True)

    _scopes = [
        "https://www.googleapis.com/auth/firebase",
        "https://www.googleapis.com/auth/datastore"
        ]

    try:
        secret_client = secretmanager.SecretManagerServiceClient()
        print(" * Secret manager initialised")

    except:
        secret_client = None
        print(" * Secret manager NOT initialised")

    if secret_client != None:
        for k, v in SECRET_URLS.items():
            var_name = "SECRET_" + k.upper()
            try:
                with open("secure/{}".format(var_name), "w") as f:
                    f.write(secret_client.access_secret_version(
                        request={"name": v}).payload.data.decode("UTF-8"))
            except:
                print(" * Error reading secret: {} from: {}".format(k, v))



def get_flask_secret():
    if not os.path.exists("secure/SECRET_FLASK"):
        database_init()
    try:
        with open("secure/SECRET_FLASK", "r") as f:
            return bytes(str(f.read()), 'utf-8')
    except:
        print(" * Failed to read flask key")
        return "I am a secret"


def database_init():
    global firebase_client
    global firebase_db
    try:
        cred = credentials.Certificate("secure/SECRET_SERVICE_ACCOUNT")
        print(" * Firebase credentials loaded from file")
    except:
        print(" * Failed to load firebase credentials")
        raise
    try:
        firebase_client = firebase_admin.initialize_app(cred)
        firebase_db = firestore.client(firebase_client, database_id="(default)")
        print(" * Firebase client initialized")
    except:
        print(" * Failed to initialize firebase client")
        raise





class FirebaseObject(object):
    bucket = None
    def __init__(self,data, id = None):
        self._data = data
        self.deleted = False
        self.hidden = False
        self.priority = 0
        for key, value in data.items():
            if type(value) is dict and hasattr(self, key):
                if type(self.__getattribute__(key)) is dict:
                    value = self.__getattribute__(key).update(value)
                    continue
            setattr(self, key, value)
        self._id = id

    def __repr__(self):
        return "\n".join(["> {}:".format(self.__class__.__name__), *["    > {} ({}): {}".format(k,type(v).__name__, v) for k,v in self.__dict__.items() if k != "data"]])+"\n"

    def __html__(self):
        return "<br>".join(["&nbsp&nbsp> {}:".format(self.__class__.__name__), *["&nbsp&nbsp&nbsp> {} ({}): {}".format(k,type(v).__name__, v) for k,v in self.__dict__.items()  if k != "data"]])+"<br>"

    def update_db(self, bucket=None):
        if bucket is None:
            bucket = self.bucket
        data = {k:v for k,v in self.__dict__.items() if not k.startswith("_")}
        data["_timestamp"] = datetime.datetime.utcnow().isoformat()
        db.collection(bucket).document(self._id).set(data)


    def keys(self):
        return list(self.__dict__.keys())

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__getattribute__(key)



class Product(FirebaseObject):
    bucket = "products"
    def __init__(self, data={}, id=None):
        self.data = {}
        self.name = None
        self.technique = None
        super().__init__(data, id)







def stream_data(bucket, data_class=FirebaseObject, as_dict=False, hidden=False, deleted=False):
    print(firebase_db)
    if firebase_db is None:
        return None
    raw = firebase_db.collection(bucket).stream()
    data = {c.id: c.to_dict() for c in raw}
    print(data)
    if as_dict:
        return data
    else:
        data = [data_class(d, id) for id, d in data.items()]
        if not deleted:
            data = [c for c in data if not c.deleted or c.deleted is None]
        if not hidden:
            data = [c for c in data if not c.hidden or c.hidden is None]
        data = sorted(data, key=lambda x: x.priority, reverse=True)
        return data



def get_products(as_dict=False, hidden=False, deleted=False):
    print("fetching products")
    return stream_data("products", as_dict=as_dict, hidden=hidden, deleted=deleted)