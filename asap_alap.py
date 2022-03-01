import argparse
import networkx as nx
import numpy as np

parser = argparse.ArgumentParser(description="calculate X to the power of Y")
group = parser.add_mutually_exclusive_group()
group.add_argument("-s", "--ASAP", help= "Run ASAP scheduling algorithm", action="store_true")
group.add_argument("-l", "--ALAP", help= "Run ALAP scheduling algorithm", action="store_true")
parser.add_argument("DAGfile", help="The DAG file path")
args = parser.parse_args()

print("DAG file is {}".format(args.DAGfile))

def ASAP(file_name):
    # build the DAG
    G = nx.DiGraph()
    G.add_node(1, t_level = 0, priority = 0, WECT=1)
    G.add_node(2, t_level = 0, priority = 0)
    G.add_node(3, t_level = 0, priority = 0)
    G.add_node(4, t_level = 0, priority = 0)
    G.add_node(5, t_level = 0, priority = 0)
    G.add_node(6, t_level = 0, priority = 0)
    G.add_node(7, t_level = 0, priority = 0)
    G.add_edge(1, 2, cost=1)
    G.add_edge(2, 4, cost=2)
    G.add_edge(3, 5, cost=1)
    G.add_edge(6, 7, cost=3)
    G.add_edge(1, 6, cost=1)
    G.add_edge(2, 3, cost=2)
    G.add_edge(4, 5, cost=1)
    G.add_edge(5, 7, cost=3)

    # find the t_level of nodes
    for node in G.nodes:
        node_prede = sorted(list(G.predecessors(node)))
        for prede in node_prede:
            temp_t_level = G.nodes[prede]['t_level']+G.get_edge_data(prede, node)['cost']
            G.nodes[node]['t_level'] = max(temp_t_level, G.nodes[node]['t_level'])
        print('Node',node,': t_level = ',G.nodes[node]['t_level'])
    
    # sort the nodes by their t_level
    node_order = sorted(G.nodes(), key=lambda n: G.nodes[n]['t_level'])

    # assign priority by t_level
    for i in range(G.order()):
        if i == 0:
            G.nodes[node_order[i]]['priority'] = 1
        else:
            if G.nodes[node_order[i]]['t_level'] == G.nodes[node_order[i-1]]['t_level']:
                G.nodes[node_order[i]]['priority'] = G.nodes[node_order[i-1]]['priority']
            else:
                G.nodes[node_order[i]]['priority'] = G.nodes[node_order[i-1]]['priority']+1
    
    # print the priority result
    for node in G.nodes:
        print('Node',node,': priority = ',G.nodes[node]['priority'])

def single_source_longest_dag_path_length(graph, s):
    dic = dict.fromkeys(graph.nodes, -float('inf'))
    dic[s] = 0
    topo_order = nx.topological_sort(graph)
    for n in topo_order:
        for s in graph.successors(n):
            dic[s] = max(dic[s], dic[n] + graph.edges[n,s]['cost'])
        dic[n] += graph.nodes[1]['WECT']
    return dic

def ALAP(file_name):
    # build the DAG
    G = nx.DiGraph()
    G.add_node(1, t_level = 0, priority = 0, WECT=1)
    G.add_node(2, t_level = 0, priority = 0)
    G.add_node(3, t_level = 0, priority = 0)
    G.add_node(4, t_level = 0, priority = 0)
    G.add_node(5, t_level = 0, priority = 0)
    G.add_node(6, t_level = 0, priority = 0)
    G.add_node(7, t_level = 0, priority = 0)
    G.add_edge(1, 2, cost=1)
    G.add_edge(2, 4, cost=2)
    G.add_edge(3, 5, cost=1)
    G.add_edge(6, 7, cost=3)
    G.add_edge(1, 6, cost=1)
    G.add_edge(2, 3, cost=2)
    G.add_edge(4, 5, cost=1)
    G.add_edge(5, 7, cost=3)

    # find the b_level of nodes
    for node in G.nodes:
        node_longest_path_dict = single_source_longest_dag_path_length(G, node)
        node_longest_path = max(node_longest_path_dict.values())
        G.nodes[node]['b_level'] = node_longest_path
        print('Node',node,': b_level = ',G.nodes[node]['b_level'])

    # sort the nodes by their b_level
    node_order = sorted(G.nodes(), key=lambda n: G.nodes[n]['b_level'])
    node_order.reverse()

    # assign priority by b_level
    for i in range(G.order()):
        if i == 0:
            G.nodes[node_order[i]]['priority'] = 1
        else:
            if G.nodes[node_order[i]]['b_level'] == G.nodes[node_order[i-1]]['b_level']:
                G.nodes[node_order[i]]['priority'] = G.nodes[node_order[i-1]]['priority']
            else:
                G.nodes[node_order[i]]['priority'] = G.nodes[node_order[i-1]]['priority']+1
    
    # print the priority result
    for node in G.nodes:
        print('Node',node,': priority = ',G.nodes[node]['priority'])

if args.ASAP:
    print("Runing ASAP")
    ASAP(args.DAGfile)
elif args.ALAP:
    print("Runing ALAP")
    ALAP(args.DAGfile)
else:
    print("Please choose the scheduling algorithm")

# if args.quiet:
#     print(answer)
# elif args.verbose:
#     print("{} to the power {} equals {}".format(args.x, args.y, answer))
# else:
#     print("{}^{} == {}".format(args.x, args.y, answer))
