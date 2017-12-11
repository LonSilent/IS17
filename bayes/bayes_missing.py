from __future__ import division, print_function
import itertools
from collections import Counter, defaultdict
import networkx as nx
import matplotlib.pyplot as plt
from bayes import *
import random

SAMPLES_COUNT = 1000000
ERR = 0.005

# random select from binary
def prob_choice_binary(key, true_count, false_count):
    all_count = true_count + false_count
    select = random.uniform(0, all_count)

    if select <= true_count:
        return 'T'
    return 'F'

# random select from triple
def prob_choice_triple(key, triple_count):
    all_count = triple_count['T'] + triple_count['B'] + triple_count['M']
    select = random.uniform(0, all_count)

    if select <= triple_count['T']:
        return 'T'
    elif select <= triple_count['T'] + triple_count['B']:
        return 'B'
    return 'M'

# fill 'NA' with probability distribution
def fill_missing(samples, valid_prob, na_count, triple_count):
    samples_count = {}
    true_count = {}
    false_count = {}

    for key, val in valid_prob.items():
        if ',' not in key:
            samples_count[key] = SAMPLES_COUNT - na_count[key]

    for key, val in valid_prob.items():
        if ',' not in key:
            true_count[key] = int(val * samples_count[key])
            false_count[key] = samples_count[key] - true_count[key]

    for i, sample in enumerate(samples):
        line = sample.split(',')
        while 'NA' in line:
            na_index = line.index('NA')
            s_index = str(na_index)
            # binary count
            if na_index != 4:
                line[na_index] = prob_choice_binary(s_index, true_count[s_index], false_count[s_index])
            # use triple count
            else:
                line[na_index] = prob_choice_triple(s_index, triple_count)
            sample = ','.join(line)
        print("{}".format(i), end='\r')

    return samples

if __name__ == '__main__':
    node_number = 1
    prob = {}
    valid_prob = {}
    samples = []
    valid_samples = []
    na_count = defaultdict(int)
    data_path = 'data/samples.2017nov071410.txt'
    missing_path = 'data/samples.missing.2017nov071410.txt'
    sample_path = 'data/samples_fill.txt'

    if node_number == 1:
        edgelist_path = 'result/edgelist_missing_order1.txt'
        node_order = ['0', '1', '2', '3', '4', '5', '6']
    elif node_number == 2:
        edgelist_path = 'result/edgelist_missing_order2.txt'
        node_order = ['1', '4', '6', '0', '5', '3', '2']

    print("Read samples...")
    with open(data_path) as f:
        column = f.readline().strip().split(',')

    with open(missing_path) as f:
        for line in f:
            line = line.strip()
            samples.append(line)
            if 'NA' not in line:
                valid_samples.append(line)
            else:
                line = line.split(',')
                na_count[str(line.index('NA'))] += 1

    # count observation    
    count_table = dict(Counter(valid_samples))
    range_subset = findsubsets(range(len(column)))
    for t in range_subset:
        t = [int(x) for x in t]
        target = tokey(t)
        valid_prob[target] = calc_prob(count_table, t)

    triple_count = defaultdict(int)
    for sample in valid_samples:
        line = sample.split(',')
        triple_count[line[4]] += 1

    print("Fill missing...")
    # fill missing with observation
    samples = fill_missing(samples, valid_prob, na_count, triple_count)

    count_table = dict(Counter(samples))
    range_subset = findsubsets(range(len(column)))
    for t in range_subset:
        t = [int(x) for x in t]
        target = tokey(t)
        prob[target] = calc_prob(count_table, t)

    print("node_order:", node_order)
    edgelist = construct_bayes_network(node_order, prob)

    # write edge list
    with open(edgelist_path, 'w') as f:
        for edge in edgelist:
            print(edge[0], edge[1], file=f)

    # draw graph
    network = nx.DiGraph()
    network.add_nodes_from([str(x) for x in range(len(node_order))])
    network.add_edges_from(edgelist)
    pos = nx.circular_layout(network)
    nx.draw(network, pos, with_labels=True, arrows=True)
    plt.show()
