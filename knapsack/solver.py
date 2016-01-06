#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import fsum
from collections import namedtuple
from copy import copy
Item = namedtuple("Item", ["index", "value", "weight", "relative"])

def safe_mult (val1, val2):
    if not val1 or not val2:
        return 0
    else:
        return val1 * val2

def value (items, decisions):
    return sum([safe_mult(decisions[i], items[i].value) for i in xrange(len(decisions))])

def size (items, decisions):
    return sum([safe_mult(decisions[i], items[i].weight) for i in xrange(len(decisions))])

def relaxation (items, decisions, capacity):
    space  = capacity - fsum([safe_mult(decisions[i], items[i].weight) for i in xrange(len(decisions))])
    relaxed_decisions = copy(decisions)
    if space < 0.0:
        return None
    if space == 0.0:
        return value(items, decisions)
    # Order the undecided items based on the ratio of value to weight
    relative_ordered = sorted([(item.relative, item) for item in items if decisions[item.index] == None])
    for item in relative_ordered:
        if space >= item[1].weight:
            relaxed_decisions[item[1].index] = 1
            space -= item[1].weight
            if space == 0.0:
                break
        else:
            relaxed_decisions[item[1].index] = space / item[1].weight
            break
    return value(items, relaxed_decisions)

# Needs to be global for the recursive function - Annoying problem solved by nonlocal statement in Python 3
best = 0
decisions_for_best = []

def solve_it (input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0]) / float(parts[1])))

    global best, decisions_for_best
    best = 0
    decisions_for_best = [None] * item_count

    def depth_first_decide (decisions, val):
        global best, decisions_for_best
        index = decisions.index(None)
        decisions = copy(decisions)
        decisions[index] = val
        if size(items, decisions) > capacity:
            return
        if index + 1 == len(decisions): #Final node
            val = value(items, decisions)
            if val > best:
                best = val
                decisions_for_best = decisions
                print decisions_for_best
        else:
            best_case = relaxation(items, decisions, capacity)
            if best_case > best:
                depth_first_decide(decisions, 1)
                depth_first_decide(decisions, 0)

    depth_first_decide([None] * len(items), 1)
    depth_first_decide([None] * len(items), 0)

    # prepare the solution in the specified output format
    output_data = str(best) + " " + str(1 if decisions_for_best[item_count - 1] else 0) + "\n"
    print decisions_for_best
    output_data += " ".join(map(str, decisions_for_best))
    return output_data

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, "r")
        input_data = "".join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print "This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)"

