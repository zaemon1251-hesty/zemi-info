from enum import Enum
import sys
from typing import Optional
from mypulp import Model, GRB, quicksum

model = Model("lptest")
v = [120, 130, 80, 100, 250, 185, 200, 50]
w = [10, 12, 7, 9, 21, 16, 18, 8]
x = [False] * 8



class Problem(Enum):
    a = "a"
    b = "b"
    c = "c"


def main(prob_name: Optional[Problem] = None):
    for i in range(8):
        x[i] = model.addVar(vtype="B", name=f"x{i}")

    model.addConstr(quicksum(xi * wi for xi, wi in zip(x, w)) <= 55)    # 体積制約

    if prob_name:
        if prob_name.value == "a":
            model.addConstr(x[4] + x[5] + x[6] <= 1)        # 主食に関する制約
        elif prob_name.value == "b":
            model.addConstr(x[2] + x[3] <= 1)        # 果物に関する制約
        elif prob_name.value == "c":
            # (x0 + (1 - x7) は (x0, x7) = (1, 0) の時のみ 1 を超える)
            model.addConstr(x[0] - x[7] <= 0)  # コーヒーに関する制約

    model.update()

    model.setObjective(quicksum(vi * xi for vi, xi in zip(v, x)), GRB.MAXIMIZE)

    model.optimize()

    print("OptVal = ", model.ObjVal)
    print(*["x{} = {}".format(i, x[i].X) for i in range(8)], sep="\n")


if __name__ == "__main__":
    # python $filepath -p a
    # というように、問題に沿う制約条件を動的に追加する
    option = "-p"
    p = None

    if option in sys.argv:
        idx = sys.argv.index(option)
        value = sys.argv[idx + 1]
        p = Problem[value]

    main(prob_name=p)
