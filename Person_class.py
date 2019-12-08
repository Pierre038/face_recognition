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


    def __init__(self, Id, faceEncoding, exists, sendPerson, image):
        self.num = Id
        self.faceEncoding = faceEncoding
        self.isActive = False
        self.exists = exists
        self.isSend = False
        self.image = image
        self.lastSeenTime = datetime.datetime(2000, 1, 1)
        if (self.exists == False and sendPerson == 0) :
            # creation et activation uniquement si aucune personne active en cours
            self.savePerson()
            self.exists = True
            verbose('__init__ creation de la personne: '+ self.num, 3)
            post(Operation.new,self.num)
            self.isActive = True

    def savePerson(self):
        writeFace(self.num, self.faceEncoding)
        writePicture(self.num, self.image)

    def sendstate(self):
        verbose('envoi de la personne: '+ self.num, 3)
        if self.isActive :
            post(Operation.knownActive,self.num)
        else:
            post(Operation.knownInactive, self.num)
    
    def activatePerson(self,time, sendPerson):
        self.lastSeenTime = time
        if not self.isActive  :
            verbose("on active la personne (sans envoi)"+ self.num, 3)
            self.isActive = True
        if sendPerson == 0:
            if self.exists:
                self.isSend = True
                self.sendstate()
            else:
                self.savePerson()
                self.exists = True
                verbose('activate creation de la personne: '+ self.num, 3)
                post(Operation.new,self.num)
                self.isActive = True
                self.isSend = True
        if self.isSend:
            return True
        else:
            return False

    def deactivatePerson(self, time):
        if(time - self.lastSeenTime) > Param.TIME_TO_INACTIVATE and self.isActive:
            verbose("la personne est partie, on la desactive "+ self.num, 3)
            self.isActive = False
            if self.isSend:
                self.sendstate()
                return True
            return False
        else:
            return False

     
