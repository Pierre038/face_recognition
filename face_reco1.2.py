import face_recognition
import cv2
import numpy as np
import os
import pickle
from array import array
from file_manipulation import *
from back_end_gestion import *
from param import *
from Person_class import *
import datetime
from utilServices import *


################################################################################################################################""
#####################  FUNCTION
################################################################################################################################""

# draw a rectangle in the frame
def printRectangleArountTheFace(name,left,top,right,bottom,frame):

    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    top *= 4
    right *= 4
    bottom *= 4
    left *= 4
    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

def checkActivity(persons,faceNames):
    global sendPerson
    for person in persons:
        if person.num in faceNames:
            if person.activatePerson(datetime.datetime.now(),sendPerson):
                sendPerson = person.num
        else:
            if person.isActive:
                if person.deactivatePerson(datetime.datetime.now()):
                    sendPerson = 0

################################################################################################################################""
#####################  FUNCTION-END
################################################################################################################################""


# Get a reference to webcam #0 (the default one)
videoCapture = cv2.VideoCapture(0 )
#video_capture = cv2.VideoCapture(1 )



knownPersons = []
idFace = 0
sendPerson = 0

initTime = datetime.datetime.now()


#searching known people from encoded face
for element in os.listdir(Param.FACE_PATH):
    verbose(element,0)
    if element.endswith('.face'):
        verbose("'%s' est un fichier visage encode" % element,0)
        faceEncoding = readFace(Param.FACE_PATH + "/" + element)
        id= element.split('.')[0]
        #recherche fichier image
        image = 'TODO'
        knownPersons.append(Person(id,faceEncoding, True,sendPerson, image))
        verbose( "le fichier a ete traite",0)
        if int(id) > idFace:
            idFace=int(id)


knownPersonNumber = len(knownPersons)
verbose("nombre de personnes connues: " + str(knownPersonNumber),3)


# Initialize some variables
faceLocations = []
faceEncodings = []
# array of persons presents in the frame:
faceNames = []
processThisFrame = True


################################################################################################################################""
#####################  END INIT
################################################################################################################################""

# affichage pendant Xs sans reconnaissance

while True:
    # Grab a single frame of video
    ret, frame = videoCapture.read()
    # Display the  image
    cv2.imshow('Video', frame)
    
    if (datetime.datetime.now() - initTime ) > Param.TIME_TO_WAIT :
        break
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
verbose('let s go!',3)


while True:

    # Grab a single frame of video
    ret, frame = videoCapture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    smallFrame = cv2.resize(frame, (0, 0), fx=Param.SCALE_DOWN, fy=Param.SCALE_DOWN)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgbSmallFrame = smallFrame[:, :, ::-1]

    # Only process every other frame of video to save time
    if processThisFrame:
        # Find all the faces and face encodings in the current frame of video
        faceLocations = face_recognition.face_locations(rgbSmallFrame)
        faceEncodings = face_recognition.face_encodings(rgbSmallFrame, faceLocations)
        faceNames = []
        index = 0
        for faceEncoding in faceEncodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(map(lambda person: person.faceEncoding, knownPersons), faceEncoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face

            faceDistances = face_recognition.face_distance(map(lambda person: person.faceEncoding, knownPersons), faceEncoding)
            bestMatchIndex = np.argmin(faceDistances)
            if matches[bestMatchIndex]:
                verbose('personne connue',0)
                name = knownPersons[bestMatchIndex].num
                if knownPersons[bestMatchIndex].activatePerson(datetime.datetime.now(),sendPerson):
                    sendPerson = name
                
            else:
                verbose('personne inconnue',2)
                idFace +=1
                name=str(idFace)
                faceLocation = faceLocations[index]
                (bottom,right,top,left) = faceLocation
                top *= 4
                bottom *= 4
                right *= 4
                left *= 4
                image = frame[bottom:top,left:right]
                knownPersons.append(Person(name, faceEncoding, False, sendPerson,image))
                sendPerson = name

            faceNames.append(name)
            index = index + 1

    processThisFrame = not processThisFrame

    # check active and inactive faces
    checkActivity(knownPersons,faceNames)

    # Display the results
    for (top, right, bottom, left), name in zip(faceLocations, faceNames):
        printRectangleArountTheFace(name,left, top, right, bottom, frame)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
videoCapture.release()
cv2.destroyAllWindows()

