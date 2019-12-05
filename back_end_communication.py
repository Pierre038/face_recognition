import requests
from utilServices import *
from enum import Enum
from param import *

class Operation(Enum):
    new = "NEW"
    known_active = "KNOWN_ACTIVE"
    known_inactive = "KNOWN_INACTIVE"

#http post
def post(operation, faceName):
    if operation.value == "NEW":
        #envoi d'un visage inconnu jusqu'ici:
        API_ENDPOINT = Param.URL + "users"
        verbose(API_ENDPOINT,0)
        # data to be sent to api 
        payload = {'_id':faceName, 
                'firstName': 'unknown', 
                'lastName':'unknown', 
                'status':'unknown'
                } 
        r = requests.post(url = API_ENDPOINT,data=payload)
        verbose(r.text,5)
    elif operation.value == "KNOWN_ACTIVE":
        #envoi d'un visage connu
        API_ENDPOINT = Param.URL + "users/" + str(faceName)
        verbose(API_ENDPOINT,0)
        payload = {}
        r = requests.post(url = API_ENDPOINT,data=payload)
        verbose(r.text,5)
    elif operation.value == "KNOWN_INACTIVE":
        verbose("fonction inactive pour le moment",99)
    else :
        verbose("fonctionnalite inconnue lors de l appel post:" + str(operation.value), 99)
   