from __future__ import division, print_function
import itertools
from collections import Counter
from operator import itemgetter
import networkx as nx
import matplotlib.pyplot as plt

SAMPLES_COUNT = 1000000
ERR = 0.005

def minimal(iterable, func):
    iterable = [set(x) for x in iterable]
    intersect = iterable[0]

    for i in range(0, len(iterable)-1):
        intersect = intersect.intersection(iterable[i+1])

    return intersect

    # lowest_values = []
    # it = iter(iterable)
    # try:
    #     x = next(it)
    # except StopIteration:
    #     return []
    # lowest_values = [x]
    # lowest_weight = func(x)
    # for x in it:
    #     weight = func(x)
    #     if weight == lowest_weight:
    #         lowest_values.append(x)
    #     elif weight < lowest_weight:
    #         lowest_values = []
    #         lowest_weight = weight
    # if len(lowest_values) == 0 and len(iterable) != 0:
    #     sort_value = set(sorted(iterable, key=len)[0])
    #     iterable_set = [set(i) for i in iterable]
    #     if all(sort_value.issubset(i) for i in iterable_set):
    #         lowest_values.append(sort_value)
    # if len(lowest_values) == 0 and len(iterable) > 1:
    #     sort_value = set(sorted(iterable, key=len)[0])
    #     lowest_values.append(sort_value)

    return intersect

def tokey(t):
    t = sorted(t)
    return ','.join([str(x) for x in t])

def findsubsets(x):
    if len(x) == 0:
        return []
    cs = findsubsets(x[1:])
    return [(x[0],)] + [(x[0],) + c for c in cs] + cs

def is_target(t, event):
    event = event.split(',')
    for c in t:
        if event[c] != 'T':
            return False
    return True

def calc_prob(count_table, target):
    event_count = 0
    for event, count in count_table.items():
        if is_target(target, event):
            event_count += count

    return event_count / SAMPLES_COUNT

def cond_p(prob, source, target):
    joint = sorted(list(set(source + target)))
    joint_p = prob[tokey(joint)]
    prior_p = prob[tokey(source)]

    return joint_p / prior_p

def check_same_p(p1, p2):
    return abs(p1 - p2) < ERR

def construct_bayes_network(node_order, prob_table):
    count = 0
    edgelist = []
    queue = []

    for node_index, node in enumerate(node_order):
        print("node:", node)
        candidates = []
        subset = findsubsets(queue)
        subset = [sorted(x) for x in subset]
        queue.append(node)
        print("queue:", queue)
        print("subset:", subset)

        if len(queue) == 1:
            print("==========================")
            continue

        # print("tokey_queue", tokey(queue))
        all_p = prob_table[tokey(queue)]
        node_p = prob_table[node]
        # print(tokey([x for x in queue if x != node]))
        all_cond_p = all_p / prob_table[tokey([x for x in queue if x != node])]
        print("all_node:", queue, "all_p:", all_p)
        print("node:", node, "node_p:", node_p)
        print("all_cond_p = given:", [x for x in queue if x != node], "target:", [node], all_cond_p)

        if len(queue) == 2:
            if not check_same_p(all_p, all_cond_p):
                edgelist.append((queue[0], node))
                print("edgelist:", edgelist)
            print("==========================")
            continue

        for s in subset:
            s = list(s)
            cp = cond_p(prob_table, s, [node])
            print("given:", s, "target:", node, "cp:", cp)
            if check_same_p(cp, all_cond_p):
                candidates.append(''.join(s))

        print("candidates:", candidates)
        self_nodes = ''.join([str(x) for x in sorted(queue) if x != node])
        print("self_nodes:", self_nodes)
        if len(candidates) > 0:
            if self_nodes in candidates:
                candidates.remove(self_nodes)
            pair = minimal(set(candidates), len)
            print("minimal set:", pair)
            if len(pair) > 0:
                for p in pair:
                    for n in p:
                        edgelist.append((n, node))
            elif check_same_p(node_p, all_cond_p):
                for n in [str(x) for x in range(int(node))]:
                    edgelist.append((n, node))
            print("edgelist:", edgelist)

        print("==========================")

    edgelist = sorted(list(set(edgelist)), key=itemgetter(0))
    return edgelist

if __name__ == '__main__':
    node_number = 4
    prob = {}
    samples = []

    if node_number == 1:
        data_path = 'data/samples.2017nov071410.txt'
        edgelist_path = 'result/edgelist_order1.txt'
        node_order = ['0', '1', '2', '3', '4', '5', '6']
    elif node_number == 2:
        data_path = 'data/samples.2017nov071410.txt'
        edgelist_path = 'result/edgelist_order2.txt'
        node_order = ['1', '4', '6', '0', '5', '3', '2']
    elif node_number == 3:
        data_path = 'data/samples.2017nov071410.txt'
        edgelist_path = 'result/edgelist_order3.txt'
        node_order = ['3', '2', '1', '0', '5', '4', '6']
    elif node_number == 4:
        data_path = 'data/is2017.testset1.txt'
        edgelist_path = 'result/edgelist_order4.txt'
        node_order = ['3', '2', '1', '0']

    with open(data_path) as f:
        column = f.readline().strip().split(',')
        for line in f:
            line = line.strip()
            samples.append(line)

    count_table = dict(Counter(samples))
    range_subset = findsubsets(range(len(column)))
    for t in range_subset:
        t = [int(x) for x in t]
        target = tokey(t)
        prob[target] = calc_prob(count_table, t)

    print("node order:", node_order)
    edgelist = construct_bayes_network(node_order, prob)

    with open(edgelist_path, 'w') as f:
        for edge in edgelist:
            print(edge[0], edge[1], file=f)

    network = nx.DiGraph()
    network.add_nodes_from([str(x) for x in range(len(node_order))])
    network.add_edges_from(edgelist)
    pos = nx.circular_layout(network)
    nx.draw(network, pos, with_labels=True, arrows=True)
    plt.show()
