from flow_log import flow_log
import json
import networkx as nx
import community

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
    flow_node_list = []
    f = open(filename, 'r')
    while True:
        log_string = f.readline()
        if not log_string:
            break
        node = build_flow_node(log_string)
        if not node:
            continue
        flow_node_list.append(node)
    return flow_node_list

def build_visual_graph(G, part, level):
    flow_log_graph = {'nodes':[], 'links':[]}
    for node in G.nodes():
        group = part[node]
        flow_log_graph['nodes'].append({'id':node, 'group':group})
    for edge in G.edges():
        flow_log_graph['links'].append({'source':edge[0], 'target':edge[1], 'value':1})

    f = open("../reljson/flow_rel_" + str(level) + ".json", "w")
    f.write(json.dumps(flow_log_graph))
    f.close()

def build_flow_graph(flow_node_list):
    G = nx.Graph()
    node_amt = len(flow_node_list)
    weight12 = 0
    #add nodes
    for i in range(node_amt):
        G.add_node(i)
    for i in range(node_amt):
        node1 = flow_node_list[i]
        for j in range(i + 1, node_amt):
            node2 = flow_node_list[j]
            weight12 = weight_between_flow_node(node1, node2)
            if weight12 > 0:
                G.add_edge(i, j, weight = weight12)
    return G