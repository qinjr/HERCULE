import time
import datetime

class node:
	def __init__(self, timestamp, duration, l4protocol, application, localip, localport, remoteip, remoteport, sendbytes, recevbytes, 
		qname, label):
		self.timestamp = timestamp
		self.duration = duration
		self.l4protocol = l4protocol
		self.localip = localip
		self.localport = localport
		self.remoteip = remoteip
		self.remoteport = remoteport
		self.sendbytes = sendbytes
		self.recevbytes = recevbytes
		self.qname = qname
		self.application = application
		self.label = label

class Hparser:
	#type:flow_l, flow_nl, resp_l, resp_nl
	def __init__(self, type):
		self.type = type

	#return a node
	def parse(self, log_string):
		if self.type == 'flow_l':
			argv = log_string.split(',')
			timestamp = time.mktime(datetime.datetime.strptime(argv[0], "%Y%m%d%H%M%S").timetuple())
			return node(timestamp, float(argv[1]), argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], int(argv[8]), int(argv[9]),
				None, int(argv[-1][0:-1]))

		if self.type == 'flow_nl':
			argv = log_string.split(',')
			timestamp = time.mktime(datetime.datetime.strptime(argv[0], "%Y%m%d%H%M%S").timetuple())
			return node(timestamp, float(argv[1]), argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], int(argv[8]), int(argv[9]),
				None, None)

		if self.type == 'resp_l':
			argv = log_string.split('\t')
			timestamp = time.mktime(datetime.datetime.strptime(argv[0], "%Y-%m-%d %H:%M:%S").timetuple())
			return node(timestamp, None, None, None, argv[2], None, argv[1], None, None, int(argv[3]), argv[-3], int(argv[-1][0:-1]))

		if self.type == 'resp_nl':
			argv = log_string.split('\t')
			timestamp = time.mktime(datetime.datetime.strptime(argv[0], "%Y-%m-%d %H:%M:%S").timetuple())
			return node(timestamp, None, None, None, argv[2], None, argv[1], None, None, int(argv[3]), argv[-3], None)


