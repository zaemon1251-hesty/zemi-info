#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2022-05-31

@author: yoichi_izunaga
"""

"""
packages
"""

#----------------#
# input data
#----------------#

from mypulp import *
import numpy as np
import itertools
data = np.loadtxt("data.csv", delimiter=",", skiprows=0)
cap = 50

# set of items
I = [
    "coffee",
    "water",
    "banana",
    "apple",
    "rice-ball",
    "bread",
    "noodle",
    "sugar",
]

# weight of each item
W = {
    "coffee": 10,
    "water": 12,
    "banana": 7,
    "apple": 9,
    "rice-ball": 21,
    "bread": 16,
    "noodle": 18,
    "sugar": 8
}

# value of each item
V = {}
for i in range(len(I)):
    for j in range(i, len(I)):
        V[I[i], I[j]] = data[i, j]
# print(V)

# enumerate all pairs of items
P = list(itertools.combinations(I, 2))
# print(P)

# setting constants
# if COMB_MODE is true, this program will also consider combinations between
# items.
COMB_MODE = True

m = Model("ex06")

# decision vars.
x = {}
for item in I:
    x[item] = m.addVar(vtype="B", name="x({})".format(item))
m.update()

# usage constraint
for i, w in W.items():
    m.addConstr(quicksum(x[item] * w for item, w in W.items()) <= cap)
m.update()


if COMB_MODE:
    # decision combination vars.
    y = {}
    for item_i, item_j in P:
        y[item_i, item_j] = m.addVar(
            vtype="B", name="x({}, {})".format(item_i, item_j))

    # usage combination constraint
    for item_i, item_j in P:
        m.addConstr(y[item_i, item_j] <= x[item_i])
        m.addConstr(y[item_i, item_j] <= x[item_j])
        m.addConstr(x[item_i] + x[item_j] <= y[item_i, item_j] + 1)
    m.update()

    m.setObjective(
        quicksum(x[item] * V[item, item] for item in I)
        + quicksum(y[item_i, item_j] * V[item_i, item_j]
                   for item_i, item_j in P),
        GRB.MAXIMIZE
    )
else:
    m.setObjective(
        quicksum(x[item] * V[item, item] for item in I),
        GRB.MAXIMIZE
    )


# print(m)


#----------------#
# solving-phase
#----------------#
m.optimize()

status = m.Status

if status == 1:
    print("Opt.Val = {}".format(m.ObjVal))
    print("OptSet = {", *[item for item, xi in x.items() if xi.X > 0], "}")


else:
    print("not-solved")
