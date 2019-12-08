import datetime

def verbose(sayIt,level):
    levelMin = 2
    sayIt = datetime.datetime.now().ctime() + ' ' + sayIt
    if level >= levelMin:
        print(sayIt)