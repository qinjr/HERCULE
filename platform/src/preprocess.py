import random
from flow_log import flow_log
import numpy as np

def label(filename):
    f = open(filename, 'r')
    f_label = open(filename[0:-4] + "_label.log", 'w')
    while True:
        log_string = f.readline()
        if not log_string:
            break
        argv = log_string.split(',')
        del(argv[-1])
        decision = random.randint(0, 7)
        if decision == 0:
            argv.append('0')
        elif decision > 0:
            argv.append('1')
        log_string = ','.join(argv)
        f_label.writelines([log_string + '\n'])

    print("finish labeling")

def build_edges_matrix(src_filename, dst_filename):
    #node_list
    f_src = open(src_filename, 'r')
    f_dst = open(dst_filename, 'w')
    node_list = []
    while True:
        log_string = f_src.readline()
        if not log_string:
            break
        argv = log_string.split(',')
        if len(argv) == 11:
            node = flow_log(argv)
            node_list.append(node)
    
    #edges matrix
    node_amt = len(node_list)
    edges_matrix = np.empty((0,5), int)

    for i in range(node_amt):
        print(i)
        node1 = node_list[i]
        for j in range(i + 1, node_amt):
            node2 = node_list[j]
            edge = [0, 0, 0, 0, 0]
            #timestamp:
            if node1.timestamp == node2.timestamp:
                edge[0] = 1
            #localip:
            if node1.localip == node2.localip:
                edge[1] = 1
            #localport:
            if node1.localport == node2.localport:
                edge[2] = 1
            #remoteip:
            if node1.remoteip == node2.remoteip:
                edge[3] = 1
            #remoteport:
            if node1.remoteport == node2.remoteport:
                edge[4] = 1
            print(edge)
            edges_matrix = np.append(edges_matrix, np.array([edge]), axis=0)
    print(edges_matrix)
    np.savetxt(f_dst, edges_matrix)

def preprocess():
    #label("../logs/flow.log")
    build_edges_matrix("../logs/flow_label.log", "../logs/flow_edges_matrix.log")



preprocess()