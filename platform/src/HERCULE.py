import tensorflow as tf
import networkx as nx
import community
import numpy as np
import time
import datetime
import math

class kdd_node:
	#_type:train(0), test(1)
	def __init__(self, log_string, _type):
		argv = log_string.split(',')
		self.starttime = time.mktime(datetime.datetime.strptime(argv[0], "%Y%m%d%H%M%S").timetuple())
		self.duration = float(argv[1])
		self.l4protocol = argv[2]
		self.application = argv[3]
		self.localip = argv[4]
		self.localport = argv[5]
		self.remoteip = argv[6]
		self.remoteport = argv[7]
		self.sendbytes = int(argv[8])
		self.recevbytes = int(argv[9])

		if _type == 0:
			self.label = int(argv[-1][0:-1])
		else:
			self.label = -1


class HERCULE:
	def __init__(self):
		self.graph = nx.Graph()
		self.alpha = np.array([[-0.06926905], [-0.00901597], [-0.81802499], [-1.04888725], [ 0.05295522], [-0.15156877], 
			[ 0.0820539 ], [ 0.89289552]])
		self.partition = {}

	#return a list of nodes
	#_type:training data(0), test data(1)
	def parse_data(self, input_file, _type):
		node_list = []
		f = open(input_file, 'r')

		while True:
			log_string = f.readline()
			if not log_string:
				break
			node = kdd_node(log_string, _type)
			node_list.append(node)
		return node_list

	def generate_relation(self, node1, node2):
		relation = [0] * 8
		if node1.starttime == node2.starttime:
			relation[0] = 1
		if node1.duration == node2.duration:
			relation[1] = 1
		if node1.l4protocol == node2.l4protocol:
			relation[2] = 1
		if node1.application == node2.application:
			relation[3] = 1
		if node1.localip == node2.localip:
			relation[4] = 1
		if node1.localport == node2.localport:
			relation[5] = 1
		if node1.remoteip == node2.remoteip:
			relation[6] = 1
		if node1.remoteport == node2.remoteport:
			relation[7] = 1
		return relation


	def format_training_data(self, input_file, output_file_x, output_file_y):
		x_list = []
		y_list = []
		node_list = self.parse_data(input_file, 0)
		node_amt = len(node_list)
		for i in range(node_amt):
			print(i)
			node1 = node_list[i]
			for j in range(i + 1, node_amt):
				node2 = node_list[j]
				relation = self.generate_relation(node1, node2)
				if relation == [0] * 8:
					continue
				x_list.append(relation)
				if node1.label == node2.label:
					y_list.append(0)
				else:
					y_list.append(1)

		np.save(output_file_x, np.array(x_list))
		np.save(output_file_y, np.array(y_list))


	def train_alpha(self, datafile_x, datafile_y):
		#alpha
		alpha = tf.Variable(tf.random_normal([8, 1]))

		#place holder
		x = tf.placeholder(tf.float32, shape=[None, 8])
		y = tf.placeholder(tf.float32, shape=[None, 1])

		#logistic regression model
		model = 1 / (1 + tf.exp(-tf.matmul(x, alpha)))

		#loss function
		loss = - tf.reduce_mean(y * tf.log(model) + (1 - y) * tf.log(1 - model))
		optimizer = tf.train.GradientDescentOptimizer(0.01)
		train = optimizer.minimize(loss)


		# training data
		x_train = np.load(datafile_x)
		y_train = np.load(datafile_y).reshape(-1, 1)
		# training loop
		init = tf.global_variables_initializer()
		sess = tf.Session()
		sess.run(init) # reset values to wrong
		for i in range(1000):
  			sess.run(train, {x: x_train, y: y_train})

  		# evaluate training accuracy
		curr_alpha, curr_loss = sess.run([alpha, loss], {x: x_train, y: y_train})
		print('current alpha: ', curr_alpha)
		print('current loss: ', curr_loss)
		self.alpha = curr_alpha

	def weight(self, relation):
		return 1 / (1 + math.exp(-np.asscalar(np.matmul(relation, self.alpha))))

	def build_graph(self, input_file):
		graph = nx.Graph()
		node_list = self.parse_data(input_file, 1)
		node_amt = len(node_list)
		for i in range(node_amt):
			graph.add_node(i)
		for i in range(node_amt):
			node1 = node_list[i]
			for j in range(i + 1, node_amt):
				node2 = node_list[j]
				relation = self.generate_relation(node1, node2)
				if relation == [0] * 8:
					continue
				weight = self.weight(np.array(relation))
				graph.add_edge(i, j, weight = weight)
		self.graph = graph

	def detect_community(self):
		dendrogram = community.generate_dendrogram(self.graph)
		partition = community.partition_at_level(dendrogram, len(dendrogram) - 1)
		self.partition = partition


	def evaluation(self, corrected_file):
		#read corrected file
		f = open(corrected_file, 'r')
		criteria = []
		while True:
			line = f.readline()
			if not line:
				break
			criteria.append(1 - int(line[-2]))
		data_amt = len(criteria)

		#all result of partition
		result = []
		for key, value in self.partition.items():
			result.append(value)

		tp, fp, fn = 0, 0, 0
		for i in range(data_amt):
			if result[i] == 0 and criteria[i] == 0:
				tp += 1
			elif result[i] == 0 and criteria[i] == 1:
				fp += 1
			elif result[i] == 1 and criteria[i] == 0:
				fn += 1

		precision = tp / (tp + fp)
		recall = tp / (tp + fn)
		F1_score = 2 * precision * recall / (precision + recall)
		print('precision: ', precision)
		print('recall', recall)
		print('F1 score: ', F1_score)




hercule = HERCULE()
#hercule.format_training_data('../logs/mini/train.log', '../logs/mini/training_datax', '../logs/mini/training_datay')
#hercule.train_alpha('../logs/mini/training_datax.npy', '../logs/mini/training_datay.npy')
hercule.build_graph('../logs/mini/test.log')
hercule.detect_community()
hercule.evaluation('../logs/mini/corrected.log')








