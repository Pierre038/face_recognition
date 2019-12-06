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

def check_activity(persons,face_names):
    global send_Person
    for person in persons:
        if person.num in face_names:
            if person.activate_person(datetime.datetime.now(),send_Person):
                send_Person = person.num
        else:
            if person.isActive:
                if person.deactivate_person(datetime.datetime.now()):
                    send_Person = 0

################################################################################################################################""
#####################  FUNCTION-END
################################################################################################################################""


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0 )
#video_capture = cv2.VideoCapture(1 )



known_Persons = []
id_face = 0
send_Person = 0


#searching known people from encoded face
for element in os.listdir(Param.FACE_PATH):
    verbose(element,0)
    if element.endswith('.face'):
        verbose("'%s' est un fichier visage encode" % element,0)
        face_encoding = readFace(Param.FACE_PATH + "/" + element)
        # known_face_encodings.append(face_encoding)
        id= element.split('.')[0]
        # known_face_names.append(id)
        known_Persons.append(Person(id,face_encoding, True,send_Person))
        verbose( "le fichier a ete traite",0)
        if int(id) > id_face:
            id_face=int(id)


knownPersonNumber = len(known_Persons)
verbose("nombre de personnes connues: " + str(knownPersonNumber),3)


# Initialize some variables
face_locations = []
face_encodings = []
# array of persons presents in the frame:
face_names = []
process_this_frame = True


################################################################################################################################""
#####################  END INIT
################################################################################################################################""

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=Param.SCALE_DOWN, fy=Param.SCALE_DOWN)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(map(lambda person: person.face_encoding, known_Persons), face_encoding)
            name = "Unknown"

            # use the known face with the smallest distance to the new face

            face_distances = face_recognition.face_distance(map(lambda person: person.face_encoding, known_Persons), face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_Persons[best_match_index].num
                if known_Persons[best_match_index].activate_person(datetime.datetime.now(),send_Person):
                    send_Person = name
                
            else:
                id_face +=1
                name=str(id_face)
                known_Persons.append(Person(name, face_encoding, False, send_Person))
                send_Person = name
                

            face_names.append(name)

    process_this_frame = not process_this_frame

    # check active and inactive faces
    check_activity(known_Persons,face_names)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        printRectangleArountTheFace(name,left, top, right, bottom, frame)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

