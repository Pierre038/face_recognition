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
    def save_Person(self):
        writeFace(self.num, self.face_encoding)

    def __init__(self, Id, face_encoding, exists):
        self.num = Id
        self.face_encoding = face_encoding
        self.isActive = False
        self.exists = exists
        if (self.exists == False) :
            self.save_Person()
        self.lastSeenTime = datetime.datetime(2000, 1, 1)

    def sendstate(self):
        post(self.num, self.isActive)
    
    def activate_person(self,time):
        self.lastSeenTime = time
        if (self.isActive == False) :
            print("on active la personne", self.num)
            self.isActive = True
            self.sendstate()

 


    def inactive_person(self, time):
        if(time - self.lastSeenTime) > Param.TIME_TO_INACTIVATE and self.isActive:
            print("la personne est partie, on la desactive", self.num,time - self.lastSeenTime)
            self.isActive = False
            self.sendstate()

     
