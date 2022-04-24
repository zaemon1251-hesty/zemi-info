#!/usr/bin/env python
# coding: utf-8

# In[2]:


from mypulp import *


# In[54]:

def main1():

    p = Model("lol")

    x1 = p.addVar(lb=0, name="x1")
    y1 = p.addVar(lb=0, name="y1")
    x2 = p.addVar(lb=0, name="x2")
    y2 = p.addVar(lb=0, name="y2")
    x3 = p.addVar(lb=0, name="x3")
    y3 = p.addVar(lb=0, name="y3")

    p.addConstr(2 * x1 + 7 * y1 <= 920)
    p.addConstr(5 * x1 + 3 * y1 <= 790)
    p.addConstr(x1 >= 30)
    p.addConstr(y1 >= 20)

    p.addConstr(2 * x2 + 7 * y2 <= 750)
    p.addConstr(5 * x2 + 3 * y2 <= 600)  # !MODIFIED 790になっていた
    p.addConstr(x2 + x1 - 30 >= 60)
    p.addConstr(y2 + y1 - 20 >= 50)

    p.addConstr(2 * x3 + 7 * y3 <= 500)
    p.addConstr(5 * x3 + 3 * y3 <= 480)
    p.addConstr(x3 + x2 + x1 - 90 >= 80)
    p.addConstr(y3 + y2 + y1 - 70 >= 90)

    p.setObjective((75 * (x1 + x2 + x3) + 50 * (y1 + y2 + y3) + 8 *
                    (x1 - 30 + x1 + x2 - 90) + 7 * (y1 - 20 + y1 + y2 - 70)), GRB.MINIMIZE)
    p.optimize()
    print("Opt.Value=", p.ObjVal)
    for v in p.getVars():
        print(v.VarName, v.X)


# In[55]:

def main2():

    q = Model("lol")

    a = [2, 7]
    b = [5, 3]
    c = [[920, 790], [750, 600], [500, 480]]
    x = [[None] * 2 for _ in range(3)]

    q.update()

    for i in range(3):
        for j in range(2):
            x[i][j] = q.addVar(lb=0)

    for i in range(3):
        q.addConstr(quicksum(a[j] * x[i][j] for j in range(2)) <= c[i][0])
        q.addConstr(quicksum(b[j] * x[i][j] for j in range(2)) <= c[i][1])

    q.addConstr(x[0][0] >= 30)
    q.addConstr(x[0][1] >= 20)
    q.addConstr(x[1][0] + (x[0][0] - 30) >= 60)
    q.addConstr(x[1][1] + (x[0][1] - 20) >= 50)
    q.addConstr(x[2][0] + (x[0][0] - 30) + (x[1][0] - 60) >= 80)
    q.addConstr(x[2][1] + (x[0][1] - 20) + (x[1][1] - 50) >= 90)

    y = [quicksum(x[i][j] for i in range(3))for j in range(2)]

    q.setObjective(
        75 * y[0] +
        50 * y[1] +
        8 * (
            2 * (
                x[0][0] - 30
            ) +
            x[1][0] - 60
        ) +
        # !MODIFIED 2倍の操作が x[1][1] - 50 にもかかっていた
        7 * (
            2 * (
                x[0][1] - 20
            ) +
            x[1][1] - 50
        ),
        GRB.MINIMIZE
    )
    q.optimize()
    print("Opt.Value=", q.ObjVal)

    for i in range(3):
        for j in range(2):
            print("{}月の製品{}の生産量＝".format(i + 1, j + 1), x[i][j].X)


if __name__ == "__main__":
    main2()
