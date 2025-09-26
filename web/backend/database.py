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

hi = 1

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