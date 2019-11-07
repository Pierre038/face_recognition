import datetime

class Param:
    # scale to improve calculation speed
    SCALE_UP = 4
    SCALE_DOWN = 0.25
    # path for face file
    FACE_PATH ='/home/pierre/Documents/project/facestock'
    #
    TIME_TO_INACTIVATE = datetime.datetime(2000,1,1,0,0,5,0) - datetime.datetime(2000,1,1,0,0,0,0)
    #
    ONLY_ONE_ACTIVE_PERSON = 1