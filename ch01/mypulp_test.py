import sys
from mypulp import Model, GRB

model = Model("lptest")

x1 = model.addVar(name="x1")
x2 = model.addVar(name="x2")
x3 = model.addVar(ub=30, name="x3")

model.update()

model.addConstr(2 * x1 + x2 + x3 <= 60)
model.addConstr(x1 + 2 * x2 + x3 <= 60)

model.setObjective(15 * x1 + 18 * x2 + 30 * x3, GRB.MAXIMIZE)

model.optimize()

print(f"x1 = {x1.X}")
print(f"x2 = {x2.X}")
print(f"x3 = {x3.X}")
print(f"Optimal Val = {model.ObjVal}")
