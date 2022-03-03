import argparse
import networkx as nx
import csv

from math import ceil
from collections import defaultdict

parser = argparse.ArgumentParser(description="Compute the priority for one directed acyclic graphs(DAG) by using ASAP or ALAP Scheduling Algorithm. (To test the program you can run the demo DAG file by 'python3 asap_alap.py -s ./DAG\ example/Tasks_1_Run_0.csv') ")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-s", "--ASAP", help="Run ASAP scheduling algorithm", action="store_true")
group.add_argument(
    "-l", "--ALAP", help="Run ALAP scheduling algorithm", action="store_true")
parser.add_argument("DAGfile", help="The DAG file path")
args = parser.parse_args()


def keepms(x):
    """
    Keep the ms as unit
    """
    return int(ceil(x))


def parse_dag_task_file(fname, scale=keepms):
    f = open(fname, 'r')
    data = csv.reader(f, skipinitialspace=True)

    periods = {}
    deadlines = {}
    nodes = defaultdict(list)

    avoid = 1

    for row in data:
        if avoid < 4:
            avoid += 1
            continue
        if row[0] == 'T':
            # parse new task declaration

            # A ’T’ row consists of the following columns:
            #
            # 	1) ’T’
            # 	2) a unique numeric ID
            # 	3) the period (in milliseconds, fractional is ok)
            # 	4) the relative deadline

            tid = int(row[1])
            p = scale(float(row[2]))
            dl = scale(float(row[3]))

            assert tid >= 0
            assert p > 0
            assert dl > 0

            periods[tid] = p
            deadlines[tid] = dl

        elif row[0] == 'V':
            # parse vertex information

            # A ‘V’ row consists for the following columns (unbounded number):
            #
            # 	1) ‘V’
            # 	2) task ID to which it belongs
            # 	3) a numeric vertex ID (unique w.r.t. its task)
            # 	4) earliest release time r^min (relative to start of period, may be zero)
            # 	5) latest release time r^max (relative to start of period)
            # 	6) BCET
            # 	7) WCET
            # 	9) first predecessor (vertex ID), if any
            # 	10) second predecessor (vertex ID), if any
            # 	11) third predecessor (vertex ID), if any
            # 	… and so on …

            tid = int(row[1])
            vid = int(row[2])

            r_min = scale(float(row[3]))
            r_max = scale(float(row[4]))
            bcet = scale(float(row[5]))
            wcet = scale(float(row[6]))
            preds = [int(pred) for pred in row[7:]]

            assert 0 <= r_min <= r_max
            assert 0 <= bcet <= wcet
            assert vid >= 0
            assert tid >= 0

            nodes[tid].append((vid, r_min, r_max, bcet, wcet, preds))
        else:
            print(row)
            assert False  # badly formatted input???

    return (periods, deadlines, nodes)

def parse_nodes_nxGraph_asap(file_name):
    periods, deadlines, nodes = parse_dag_task_file(file_name)
    G = nx.DiGraph()
    nodes = nodes.get(1)
    print(nodes)
    for node in nodes:
        index = node[0]
        WCET_temp = node[4]
        if(index == 1):
            G.add_node(index, t_level = 0, priority = 0, WCET=WCET_temp)
        else:
            G.add_node(index, t_level = 0, priority = 0)
        print("Add node {} to Graph".format(index))
        for pred in node[5]:
            G.add_edge(pred, index, cost=nodes[pred-1][4])
            print("Add edge from node {} to {} with cost:{}".format(pred, index, nodes[pred-1][4]))
    return G

def parse_nodes_nxGraph_alap(file_name):
    periods, deadlines, nodes = parse_dag_task_file(file_name)
    G = nx.DiGraph()
    nodes = nodes.get(1)
    for node in nodes:
        index = node[0]
        WCET_temp = node[4]
        if(index == 1):
            G.add_node(index, b_level = 0, priority = 0, WCET=WCET_temp)
        else:
            G.add_node(index, b_level = 0, priority = 0)
        print("Add node {} to Graph".format(index))
        for pred in node[5]:
            G.add_edge(pred, index, cost=nodes[pred-1][4])
            print("Add edge from node {} to {} with cost:{}".format(pred, index, nodes[pred-1][4]))
    return G

def ASAP(file_name):
    # build the DAG
    G = parse_nodes_nxGraph_asap(file_name)
    # find the t_level of nodes
    print("-----t_level of nodes:-----")
    for node in G.nodes:
        node_prede = sorted(list(G.predecessors(node)))
        for prede in node_prede:
            temp_t_level = G.nodes[prede]['t_level'] + \
                G.get_edge_data(prede, node)['cost']
            G.nodes[node]['t_level'] = max(
                temp_t_level, G.nodes[node]['t_level'])
        print('Node', node, ': t_level = ', G.nodes[node]['t_level'])

    # sort the nodes by their t_level
    node_order = sorted(G.nodes(), key=lambda n: G.nodes[n]['t_level'])

    # assign priority by t_level
    for i in range(G.order()):
        if i == 0:
            G.nodes[node_order[i]]['priority'] = 1
        else:
            if G.nodes[node_order[i]]['t_level'] == G.nodes[node_order[i-1]]['t_level']:
                G.nodes[node_order[i]
                        ]['priority'] = G.nodes[node_order[i-1]]['priority']
            else:
                G.nodes[node_order[i]
                        ]['priority'] = G.nodes[node_order[i-1]]['priority']+1

    # print the priority result
    print("-----priority of nodes:-----")
    for node in G.nodes:
        print('Node', node, ': priority = ', G.nodes[node]['priority'])


def single_source_longest_dag_path_length(graph, s):
    dic = dict.fromkeys(graph.nodes, -float('inf'))
    dic[s] = 0
    topo_order = nx.topological_sort(graph)
    for n in topo_order:
        for s in graph.successors(n):
            dic[s] = max(dic[s], dic[n] + graph.edges[n, s]['cost'])
        dic[n] += graph.nodes[1]['WCET']
    return dic


def ALAP(file_name):
    # build the DAG
    G = parse_nodes_nxGraph_alap(file_name)

    # find the b_level of nodes
    print("-----b_level of nodes:-----")
    for node in G.nodes:
        node_longest_path_dict = single_source_longest_dag_path_length(G, node)
        node_longest_path = max(node_longest_path_dict.values())
        G.nodes[node]['b_level'] = node_longest_path
        print('Node', node, ': b_level = ', G.nodes[node]['b_level'])

    # sort the nodes by their b_level
    node_order = sorted(G.nodes(), key=lambda n: G.nodes[n]['b_level'])
    node_order.reverse()

    # assign priority by b_level
    for i in range(G.order()):
        if i == 0:
            G.nodes[node_order[i]]['priority'] = 1
        else:
            if G.nodes[node_order[i]]['b_level'] == G.nodes[node_order[i-1]]['b_level']:
                G.nodes[node_order[i]
                        ]['priority'] = G.nodes[node_order[i-1]]['priority']
            else:
                G.nodes[node_order[i]
                        ]['priority'] = G.nodes[node_order[i-1]]['priority']+1

    # print the priority result
    print("-----priority of nodes:-----")
    for node in G.nodes:
        print('Node', node, ': priority = ', G.nodes[node]['priority'])


print("DAG file is {}".format(args.DAGfile))

if args.ASAP:
    print("-----Runing ASAP-----")
    ASAP(args.DAGfile)
elif args.ALAP:
    print("-----Runing ALAP-----")
    ALAP(args.DAGfile)
else:
    print("Please choose the scheduling algorithm.")

