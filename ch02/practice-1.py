import sys
from mypulp import Model, GRB, quicksum

model = Model("lptest")
b = [.3, .3, .4]
A = [
    [.2, .5, .3, .3, .3, .6, .4, .1, .1],
    [.3, .4, .2, .4, .3, .3, .5, .3, .1],
    [.5, .1, .5, .3, .4, .1, .1, .6, .8]
]
c = [7.3, 6.9, 7.3, 7.5, 7.6, 6.0, 5.8, 4.3, 4.1]
x = []
for i in range(9):
    x.append(model.addVar(ub=1, lb=0, name=f"x{i}"))

model.addConstr(quicksum(xi for xi in x) == 1)

for j in range(3):
    model.addConstr(quicksum(xi * aij for xi, aij in zip(x, A[j])) == b[j])

model.update()

model.setObjective(quicksum(ci * xi for ci, xi in zip(c, x)), GRB.MINIMIZE)

model.optimize()

for xi in x:
    print(xi.X)
print(f"Optimal Val = {model.ObjVal}")
