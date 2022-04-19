import sys
from mypulp import Model, GRB, quicksum

model = Model("lptest")
A = [
    [2, 7],
    [5, 3],
]
C = [
    [75, 50],
    [8, 7],
]
B = [
    [30, 20],
    [60, 50],
    [80, 90]
]
D = [
    [920, 790],
    [750, 600],
    [500, 480]
]


x = []
for i in range(3):
    xx = []
    for j in range(2):
        # 制約 X >= B
        xx.append(model.addVar(lb=B[i][j], name=f"x{i}_{j}"))
    x.append(xx)


for i in range(3):
    # 月 (1 ~ 3)
    for j in range(2):
        # 原料 (A ~ B)

        # 制約 XA <= D
        model.addConstr(
            quicksum(
                xij * aji
                for xij, aji in zip(x[i], [A[0][j], A[1][j]])
            ) <= D[i][j]
        )

model.update()

model.setObjective(quicksum(ci * xi for ci, xi in zip(C, x)), GRB.MINIMIZE)

model.optimize()

for xi in x:
    print(xi.X)
print(f"Optimal Val = {model.ObjVal}")
