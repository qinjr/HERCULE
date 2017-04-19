import pyshark
import networkx as nx
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.graph_objs import *

cap = pyshark.FileCapture("httpPkts.pcapng", display_filter = "http", only_summaries = True)
G = nx.Graph()
maxTimeGap = 0.001
pktsList = []

#----------------------------Main Functions to Generate the Graph----------------------------#
def buildList():
    global pktsList
    for pkt in cap:
        pktsList.append(pkt)

def giveWeight(pkt1, pkt2):
    weight = 0
    #feature1:timeGap
    timeGap = abs(float(pkt1.time) - float(pkt2.time))
    if (timeGap < maxTimeGap):
        weight += 1
    
    #feature2:destination ip
    pkt1Dst = pkt1.destination
    pkt2Dst = pkt2.destination
    if (pkt1Dst == pkt2Dst):
        weight += 1

    return weight

def buildGraph():
    global G
    pktsListLength = len(pktsList)
    for i in range(pktsListLength):
        pkt1 = pktsList[i]
        for j in range(i + 1, pktsListLength):
            pkt2 = pktsList[j]
            weight12 = giveWeight(pkt1, pkt2)
            if (weight12 > 0):
                G.add_node(pkt1.time, dstip = pkt1.destination)
                G.add_node(pkt2.time, dstip = pkt2.destination)
                G.add_edge(pkt1.time, pkt2.time, weight = weight12)
            else:
                G.add_node(pkt1.time, dstip = pkt1.destination)
                G.add_node(pkt2.time, dstip = pkt2.destination)


#----------------------------Helper Functions to plot on plot.ly----------------------------#
def scatter_edges(G, pos, line_color=None, line_width=1):
    trace = Scatter(x=[], y=[], mode='lines')
    for edge in G.edges():
        trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]
        trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]  
        trace['hoverinfo']='none'
        trace['line']['width']=line_width
        if line_color is not None: # when it is None a default Plotly color is used
            trace['line']['color']=line_color
    return trace 

def scatter_nodes(pos, labels=None, color=None, size=10, opacity=1):
    # pos is the dict of node positions
    # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
    # color is the color for nodes. When it is set as None the Plotly default color is used
    # size is the size of the dots representing the nodes
    #opacity is a value between [0,1] defining the node color opacity
    trace = Scatter(x=[], y=[],  mode='markers', marker=Marker(size=[]))
    for k in pos:
        trace['x'].append(pos[k][0])
        trace['y'].append(pos[k][1])
    attrib=dict(name='', text=labels , hoverinfo='text', opacity=opacity) # a dict of Plotly node attributes
    trace=dict(trace, **attrib)# concatenate the dict trace and attrib
    trace['marker']['size']=size
    return trace


buildList()
buildGraph()

position=nx.spring_layout(G)
traceE=scatter_edges(G, position)
traceN=scatter_nodes(position)
data1=Data([traceE, traceN])
fig = Figure(data=data1)
py.plot(fig, filename='testGraph')

#node_labels = nx.get_node_attributes(G,'dstip')
#edge_labels = nx.get_edge_attributes(G,'weight')
#nx.draw_networkx_labels(G, pos, labels = node_labels)
#nx.draw_networkx_edge_labels(G, pos, labels = edge_labels)
#nx.draw(G)
#plt.show()

