from platform import *
import datetime

def main():
    flow_node_list = load_flow_nodes("../mini_logs/flow_log_mini.log")
    start = datetime.datetime.now()
    G = build_flow_graph(flow_node_list)
    stop = datetime.datetime.now()
    print("time of build_flow_graph:", stop - start)

    start = datetime.datetime.now()
    dendrogram = community.generate_dendrogram(G)
    stop = datetime.datetime.now()
    print("time of community.generate_dendrogram:", stop - start)
    
    for level in range(len(dendrogram)):
        start = datetime.datetime.now()
        part = community.partition_at_level(dendrogram, level)
        stop = datetime.datetime.now()
        print("time of community.partition_at_level:", stop - start)

        start = datetime.datetime.now()
        visualG = community.induced_graph(part, G)
        stop = datetime.datetime.now()
        print("time of community.induced_graph:", stop - start)

        start = datetime.datetime.now()
        build_visual_graph(visualG, level)
        stop = datetime.datetime.now()
        print("time of build_visual_graph:", stop - start)
        print("---------------------------------------------")

main()