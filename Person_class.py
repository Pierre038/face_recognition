from file_manipulation import *
from back_end_communication import *
from services import *
import datetime
from param import *
from utilServices import *

#class Person
#properties
#   Id
#   face_encoding
#   isActive
#   lastActiveTime
#   exists
# methods
#   contructor:(Id,face_encoding,exists)
#       setId, face_encoding
#       set isActive to false
#       set lastActiveTime to 01011901
#   sendActivestate
#       send http request
#       set isActive to true
#       set lastactiveTime to now
#   sendInactiveState
#       send http request
#       set isActive to false
#   savePerson (private)
#       write a file id.face with face_encoding
class Person:


    def __init__(self, Id, face_encoding, exists,sendPerson):
        self.num = Id
        self.face_encoding = face_encoding
        self.isActive = False
        self.exists = exists
        self.isSend = False
        self.lastSeenTime = datetime.datetime(2000, 1, 1)
        if (self.exists == False and sendPerson == 0) :
            # creation et activation uniquement si aucune personne active en cours
            self.save_Person()
            post(Operation.new,self.num)
            self.exists = True

    def save_Person(self):
        writeFace(self.num, self.face_encoding)

    def sendstate(self):
        verbose('envoi de la personne: '+ self.num, 1)
        if self.isActive :
            post(Operation.known_active,self.num)
        else:
            post(Operation.known_inactive, self.num)
    
    def activate_person(self,time, sendPerson):
        self.lastSeenTime = time
        if (self.isActive == False) :
            verbose("on active la personne"+ self.num, 1)
            self.isActive = True
        if sendPerson == 0:
            self.isSend = True
            self.sendstate()
        if self.isSend:
            return True
        else:
            return False

    def deactivate_person(self, time):
        if(time - self.lastSeenTime) > Param.TIME_TO_INACTIVATE and self.isActive and self.isSend:
            verbose("la personne est partie, on la desactive"+ self.num, 1)
            self.isActive = False
            self.sendstate()
            return True
        else:
            return False

     
