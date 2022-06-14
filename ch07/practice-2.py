#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from mypulp import Model, GRB, quicksum
import numpy as np

PRIMARY = True
if len(sys.argv) >= 2:
    print(sys.argv)
    PRIMARY = bool(sys.argv[1] != "False")


model = Model("lptest")

b = [3, 4, 2]

A = [
    [2, 0, 0],
    [1, 0, 2],
    [0, 3, 1]
]

c = [4, 8, 6]

if PRIMARY:
    x = []
    for i in range(3):
        x.append(model.addVar(vtype="C", name=f"x{i}"))

    for j in range(3):
        model.addConstr(quicksum(xi * aij for xi, aij in zip(x, A[j])) <= c[j])

    model.update()

    model.setObjective(quicksum(bi * xi for bi, xi in zip(b, x)), GRB.MAXIMIZE)
    model.optimize()

    for xi in x:
        print(f"{xi.name} = {xi.X}")
    print(f"Optimal Val = {model.ObjVal}")

else:
    y = []
    # 転置
    At = np.asarray(A).T.tolist()
    print(A)
    for i in range(3):
        y.append(model.addVar(vtype="C", name=f"y{i}"))

    for j in range(3):
        model.addConstr(
            quicksum(
                yi * atij for yi, atij in zip(y, At[j])
            ) >= b[j]
        )

    model.update()

    model.setObjective(quicksum(ci * yi for ci, yi in zip(c, y)), GRB.MINIMIZE)
    model.optimize()

    for yi in y:
        print(f"{yi.name} = {yi.X}")
    print(f"Optimal Val = {model.ObjVal}")
