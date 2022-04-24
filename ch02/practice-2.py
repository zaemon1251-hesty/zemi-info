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


X = []
# X1 = {X[1:, :] - B[1:, :]}
# X2 = {X[2:, :] - B[2:, :]}
# vacants are filled with 0

for i in range(3):
    xx = []
    for j in range(2):
        xx.append(model.addVar(name=f"x{i}_{j}"))
    X.append(xx)

# 制約  (X + X1 + X2) >= B


for i in range(3):
    # 月 (1 ~ 3)
    for j in range(2):
        # 原料 (A ~ B)

        # 制約 XA <= D
        model.addConstr(
            quicksum(
                xij * aji
                for xij, aji in zip(X[i], [A[0][j], A[1][j]])
            ) <= D[i][j]
        )

model.update()

model.setObjective(quicksum(xi * ci for xi, ci in zip(X, C)), GRB.MINIMIZE)

model.optimize()

for xi in X:
    print(xi.X)
print(f"Optimal Val = {model.ObjVal}")
