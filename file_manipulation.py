import pickle
from param import *


def writeFace(name, face):
    file_name=name+'.face'
    file=open(Param.FACE_PATH + "/" + file_name,'wb')
    pickle.dump(face,file)
    file.close()

def readFace(file_name):
    file = open(file_name,'rb')
    encoded_face = pickle.load(file)
    file.close()
    return encoded_face