import pyshark
import json

cap = pyshark.FileCapture("httpPkts.pcapng", display_filter = "http", only_summaries = True)
G = {'nodes':[], 'links':[]}
maxTimeGap = 0.001
pktsList = []

def buildList():
    global pktsList
    for pkt in cap:
        pktsList.append(pkt)

def giveWeight(pkt1, pkt2):
    weight = 0
    #feature1:timeGap
    timeGap = abs(float(pkt1.time) - float(pkt2.time))
    if timeGap < maxTimeGap:
        weight += 1
    
    #feature2:destination ip
    pkt1Dst = pkt1.destination
    pkt2Dst = pkt2.destination
    if pkt1Dst == pkt2Dst:
        weight += 1
    return weight

def buildGraph():
    global G
    pktsListLength = len(pktsList)
    #add nodes
    for i in range(pktsListLength):
        G['nodes'].append({'id':pktsList[i].time})
    for i in range(pktsListLength):
        pkt1 = pktsList[i]
        for j in range(i + 1, pktsListLength):
            pkt2 = pktsList[j]
            weight12 = giveWeight(pkt1, pkt2)
            if weight12 > 0:
                G['links'].append({'source':pkt1.time, 'target':pkt2.time, 'value':weight12})

buildList()
buildGraph()
f = open("rel.json", "w")
f.write(json.dumps(G))
f.close()


