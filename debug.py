from datetime import datetime


class Debug:
    def __init__(self,script,level=1,file=None):
        ### Constructor of the debug class. file will be optional. If defined, debug will be writen to a file
        ### In case it is not defined, it will be just printed
        ### script: is the name of the script
        ### level: is the level (1 - all, 2 - warning, 3-error)
        self.script=script
        self.level=level
        self.file=file

    def msg(self,action,objecttype,object,level,*details):
        ### message to file or printed
        # If level is less than self level, nothing will be printed
        if level < self.level:
            return True
        detalles=""
        for ar in details:
            detalles=detalles+"["+ar+"]"
        if detalles=='':
            detalles='[NA]'
        print("["+str(datetime.now())+"]"+
            "[" + self.script + "]"+
            "[Level: " + str(level) + "]" +
            "[" + action + "]" +
            "[" + objecttype + "]" +
            "[" + object + "]" +
            detalles)
        return True