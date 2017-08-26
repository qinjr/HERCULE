import tensorflow as tf
import networkx as nx
import community
import numpy as np
import time
import datetime
import math
from Hparser import *
import os


FEATURE_NUM = 9
TIME_DELTA = 0
DURATION_DELTA = 0

class HERCULE:
	def __init__(self):
		self.graph = nx.Graph()
		self.alpha = np.array([[-0.43575451], [ 0.02100873], [-0.3990829 ], [-1.43498302], [ 0.90139693], [-0.49796343],
			[ 0.25010577], [-0.35445565], [ 0.76627266]])
		self.partition = {}

	#return a list of nodes
	#_type:flow_l, flow_nl, resp_l, resp_nl
	def parse_data(self, input_file, _type):
		parser = Hparser(_type)
		node_list = []
		f = open(input_file, 'r')

		while True:
			log_string = f.readline()
			if not log_string:
				break
			node = parser.parse(log_string)
			node_list.append(node)
		return node_list

	def generate_relation(self, node1, node2, time_delta, duration_delta):
		relation = [0] * FEATURE_NUM
		if abs(node1.timestamp - node2.timestamp) <= time_delta:
			relation[0] = 1
		if node1.duration and node2.duration and abs(node1.duration - node2.duration) <= duration_delta:
			relation[1] = 1
		if node1.l4protocol and node2.l4protocol and node1.l4protocol == node2.l4protocol:
			relation[2] = 1
		if node1.application and node2.application and node1.application == node2.application:
			relation[3] = 1
		if node1.localip and node2.localip and node1.localip == node2.localip:
			relation[4] = 1
		if node1.localport and node2.localport and node1.localport == node2.localport:
			relation[5] = 1
		if node1.remoteip and node2.remoteip and node1.remoteip == node2.remoteip:
			relation[6] = 1
		if node1.remoteport and node2.remoteport and node1.remoteport == node2.remoteport:
			relation[7] = 1
		if node1.qname and node2.qname and node1.qname == node2.qname:
			relation[8] = 1
		return relation


	def format_training_data(self, input_type, input_file, output_file_x, output_file_y):
		x_list = []
		y_list = []
		node_list = self.parse_data(input_file, input_type)
		node_amt = len(node_list)
		for i in range(node_amt):
			node1 = node_list[i]
			for j in range(i + 1, node_amt):
				node2 = node_list[j]
				relation = self.generate_relation(node1, node2, TIME_DELTA, DURATION_DELTA)
				if relation == [0] * FEATURE_NUM:
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
		alpha = tf.Variable(tf.random_normal([FEATURE_NUM, 1]))

		#place holder
		x = tf.placeholder(tf.float32, shape=[None, FEATURE_NUM])
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

	def build_graph(self, input_file_list, input_type_list):
		graph = nx.Graph()
		node_list = []
		for i in range(len(input_file_list)):
			input_file = input_file_list[i]
			input_type = input_type_list[i]
			node_list += self.parse_data(input_file, input_type)

		node_amt = len(node_list)
		for i in range(node_amt):
			graph.add_node(i)
		for i in range(node_amt):
			node1 = node_list[i]
			for j in range(i + 1, node_amt):
				node2 = node_list[j]
				relation = self.generate_relation(node1, node2, TIME_DELTA, DURATION_DELTA)
				if relation == [0] * FEATURE_NUM:
					continue
				weight = self.weight(np.array(relation))
				graph.add_edge(i, j, weight = weight)
		self.graph = graph

	def detect_community(self):
		dendrogram = community.generate_dendrogram(self.graph)
		partition = community.partition_at_level(dendrogram, len(dendrogram) - 1)
		print(partition)
		self.partition = partition


	def evaluation(self, corrected_file_list):
		#read corrected file
		criteria = []
		for corrected_file in corrected_file_list:
			f = open(corrected_file, 'r')
			while True:
				line = f.readline()
				if not line:
					break
				criteria.append(1 - int(line[-2]))
			f.close()
		data_amt = len(criteria)

		#all result of partition
		result = []
		for key, value in self.partition.items():
			result.append(value)
		print(len(result))

		tp, fp, tn, fn = 0, 0, 0, 0
		for i in range(data_amt):
			if result[i] == 0 and criteria[i] == 0:
				tp += 1
			elif result[i] == 0 and criteria[i] == 1:
				fp += 1
			elif result[i] == 1 and criteria[i] == 0:
				fn += 1
			else:
				tn += 1

		print(tp, fp, tn, fn)
		precision = tp / (tp + fp)
		recall = tp / (tp + fn)
		F1_score = 2 * precision * recall / (precision + recall)
		print('precision: ', precision)
		print('recall', recall)
		print('F1 score: ', F1_score)



def main():
	hercule = HERCULE()
	datadir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.path.sep + 'data' + os.path.sep + 'sjtu_flow' + os.path.sep + 'mini'
	"""
	#format training data
	hercule.format_training_data('flow_l', datadir + os.path.sep + 'train.log', datadir + os.path.sep + 'training_datax', 
		datadir + os.path.sep + 'training_datay')

	#train_alpha
	hercule.train_alpha(datadir + os.path.sep + 'training_datax.npy', datadir + os.path.sep + 'training_datay.npy')
	"""

	#test
	test_file_list = [datadir + os.path.sep + 'flow_test1.log', datadir + os.path.sep + 'resp_test1.log']
	test_type_list = ['flow_nl', 'resp_nl']

	hercule.build_graph(test_file_list, test_type_list)
	hercule.detect_community()

	#evaluation
	corrected_file_list = [datadir + os.path.sep + 'flow_corrected1.log', datadir + os.path.sep + 'resp_corrected1.log']
	hercule.evaluation(corrected_file_list)

if __name__ == '__main__':
	main()


