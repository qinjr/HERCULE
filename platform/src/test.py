from platform import *

def main():
    flow_node_list = load_flow_nodes("../mini_logs/flow_log_mini.log")
    G = build_flow_graph(flow_node_list)
    dendrogram = community.generate_dendrogram(G)
    for level in range(len(dendrogram)):
        part = community.partition_at_level(dendrogram, level)
        visualG = community.induced_graph(part, G)
        build_visual_graph(visualG, part, level)

main()