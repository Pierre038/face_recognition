from file_manipulation import *
from back_end_communication import *
from services import *
import datetime
from param import *


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


    def __init__(self, Id, face_encoding, exists):
        self.num = Id
        self.face_encoding = face_encoding
        self.isActive = False
        self.exists = exists
        self.isSend = False
        if (self.exists == False) :
            self.save_Person()
        self.lastSeenTime = datetime.datetime(2000, 1, 1)

    def save_Person(self):
        writeFace(self.num, self.face_encoding)

    def sendstate(self):
        print('envoi de la personne: ', self.num)
        post(self.num, self.isActive)
    
    def activate_person(self,time, sendPerson):
        self.lastSeenTime = time
        if (self.isActive == False) :
            print("on active la personne", self.num)
            self.isActive = True
        if sendPerson == 0:
            self.isSend = True
            self.sendstate()
        if self.isSend:
            return True
        else:
            return False

    def inactive_person(self, time):
        if(time - self.lastSeenTime) > Param.TIME_TO_INACTIVATE and self.isActive and self.isSend:
            print("la personne est partie, on la desactive", self.num)
            self.isActive = False
            self.sendstate()
            return True
        else:
            return False

     
