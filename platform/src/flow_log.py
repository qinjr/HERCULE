import datetime
import time
class flow_log:
    timestamp = 0
    duration = 0
    l4protocol = ""
    application = ""
    localip = ""
    localport = 0
    remoteip = ""
    remoteport = 0
    sendbytes = 0
    recvbytes = 0
    label = 0

    def __init__(self, argv):
        self.timestamp = time.mktime(datetime.datetime.strptime(argv[0], "%Y%m%d%H%M%S").timetuple())
        self.duration = float(argv[1]);
        self.l4protocol = argv[2];
        self.application = argv[3];
        self.localip = argv[4];
        self.localport = int(argv[5]);
        self.remoteip = argv[6];
        self.remoteport = int(argv[7]);
        self.sendbytes = int(argv[8]);
        self.recvbytes = int(argv[9]);
        self.label = int(argv[10][0:-1])