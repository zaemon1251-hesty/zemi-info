#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2022-04-26

@author: yoichi_izunaga
"""
import numpy as np
from mypulp import *

"""
packages
"""

#----------------#
# input data
#----------------#

# list of production
P = ["p1", "p2"]

# list of months
T = ["Jan", "Feb", "Mar"]

# dict. of
U = {
    "p1": (2, 5),
    "p2": (7, 3)
}

C = {
    "p1": (75, 8),
    "p2": (50, 7)
}

S = {
    ("Jan", "p1"): 30,
    ("Jan", "p2"): 20,
    ("Feb", "p1"): 60,
    ("Feb", "p2"): 50,
    ("Mar", "p1"): 80,
    ("Mar", "p2"): 90,
}

D = {
    "Jan": (920, 790),
    "Feb": (750, 600),
    "Mar": (500, 480)
}

#----------------#
# generate opt. model
#----------------#
m = Model("ex01_2")

# decision vars.
x = {}
for p in P:
    for t in T:
        x[p, t] = m.addVar(vtype="C", lb=0.0, name="x({},{})".format(p, t))
y = {}
for p in P:
    for t in T:
        y[p, t] = m.addVar(vtype="C", lb=0.0, name="y({},{})".format(p, t))
m.update()

# usage constraint
for t in T:  # month
    for j in range(2):  # material
        m.addConstr(quicksum(U[p][j] * x[p, t] for p in P) <= D[t][j])

for i, t in enumerate(T):
    prev_t = T[i - 1]

    if i == 0:
        prev_t = None

    if prev_t is not None:
        for p in P:
            m.addConstr(x[p, t] - y[p, t] + y[p, prev_t] == S[t, p])
    else:
        for p in P:
            m.addConstr(x[p, t] - y[p, t] == S[t, p])


m.update()

m.setObjective(
    quicksum(C[p][0] * x[p, t] for t in T for p in P)
    + quicksum(C[p][1] * y[p, t] for t in T for p in P),
    GRB.MINIMIZE
)

#----------------#
# solving-phase
#----------------#
m.optimize()

status = m.Status

if status == 1:
    print("Opt.Val = {}".format(m.ObjVal))
    for t in T:
        print(t)
        for p in P:
            print("prod:{}, \t stock:{}".format(x[p, t].X, y[p, t].X))

else:
    print("not-solved")
