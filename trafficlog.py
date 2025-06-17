from whad.common.monitors import PcapWriterMonitor
from datetime import datetime
from os import symlink, mkdir, remove
from os.path import isdir, join, islink

PCAPS_FOLDER = "pcaps"
LINK_NAME = "lastTL"
DATE_FORMAT=r"%d%m%y_%H:%M:%S"

class TrafficLogger() :
    def __init__(self, connector) :
        self.setupfolder()
        self.isOK = True
        self.filename = self.getafilename()
        self.Monitor = PcapWriterMonitor(self.filename)
        self.Monitor.attach(connector)
        self.Monitor.start()


    def setupfolder(self) :
        if not isdir(PCAPS_FOLDER) :
            try : mkdir(PCAPS_FOLDER)
            except Exception as e : 
                print(f"TL setup failed : {e}")
                exit(-1)
    
    def getafilename(self) :
        t = datetime.now() 
        path =  t.strftime(DATE_FORMAT)+".pcap"
        path = join(PCAPS_FOLDER, path) 
        return path
    
    def toggle(self) :
        self.isOK = not self.isOK

    def finish(self) :
        self.Monitor.detach()
        self.Monitor.stop()
        self.Monitor.close()
        if(self.isOK==False) : remove(self.filename)
        else :
            if(islink(LINK_NAME)) : remove(LINK_NAME)
            symlink(self.filename, LINK_NAME) 
            print(f"> Traffic Logged in : {self.filename}")
        


if(__name__=="__main__") :
   pass