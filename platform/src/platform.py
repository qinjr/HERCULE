from flow_log import flow_log
import json
flow_node_list = []
flow_log_graph = {'nodes':[], 'links':[]}

def parser(log_string):
    argv = log_string.split(',')
    return argv

def build_flow_node(log_string):
    argv = parser(log_string)
    if len(argv) == 11:
        node = flow_log(argv)
        return node
    return

def weight_between_flow_node(node1, node2):
    weight = 0
    #timestamp:
    if node1.timestamp == node2.timestamp:
        weight += 1
    #localip:
    if node1.localip == node2.localip:
        weight += 1
    #localport:
    if node1.localport == node2.localport:
        weight += 1
    #remoteip:
    if node1.remoteip == node2.remoteip:
        weight += 1
    #remoteport:
    if node1.remoteport == node2.remoteport:
        weight += 1
    return weight

def load_flow_nodes(filename):
    f = open(filename, 'r')
    while True:
        log_string = f.readline()
        if not log_string:
            break
        node = build_flow_node(log_string)
        if not node:
            continue
        flow_node_list.append(node)

def build_graph():
    node_amt = len(flow_node_list)
    weight = 0
    #add nodes
    for i in range(node_amt):
        flow_log_graph['nodes'].append({'id':i, 'group':1})
    #add links
    for i in range(node_amt):
        node1 = flow_node_list[i]
        for j in range(i + 1, node_amt):
            node2 = flow_node_list[j]
            weight = weight_between_flow_node(node1, node2)
            if weight > 0:
                flow_log_graph['links'].append({'source':i, 'target':j, 'value':weight})

load_flow_nodes("../mini_logs/flow_log_mini.log")
build_graph()
f = open("../reljson/flow_rel.json", "w")
f.write(json.dumps(flow_log_graph))
f.close()