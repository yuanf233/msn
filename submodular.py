import gurobipy as gp
import random
import math

file = open("facebook_combined.txt", "r")
lines = file.readlines()
file.close()
relation = {}
valuation = {}

for line in lines:
    line = line.strip()
    split_line = line.split(" ")
    if relation.get(split_line[0]) is None:
        relation[split_line[0]] = [split_line[1]]
    else:
        relation[split_line[0]].append(split_line[1])
    if relation.get(split_line[1]) is None:
        relation[split_line[1]] = [split_line[0]]
    else:
        relation[split_line[1]].append(split_line[0])

'''
def generate(m, max_value):
    array = list(range(1, max_value))
    subsets = []
    for i in range(m):
        sample = random.randint(1, int(max_value / 1.5)) + 20
        subset = set(random.sample(array, sample))
        subsets.append(subset)
    res = []
    for i in range(1, 2 ** m):
        k = i
        j = 0
        tmp = set()
        flag = False
        while k:
            if k % 2 == 1:
                if flag == False:
                    tmp = subsets[j]
                    flag = True
                else:
                    tmp = tmp.union(subsets[j])
            k = k >> 1
            j = j + 1
        res.append(len(tmp))
    return res


file = open("value_case5_hamsterster_6.txt", "w")
generate(6, 400000)

for key in relation.keys():
    valuation[key] = generate(6, random.randint(50, 40000))
    file.write(key+" ")
    for i in range(len(valuation[key])):
        file.write(str(valuation[key][i])+" ")
    file.write('\n')


'''

file = open("value_case5_facebook_5.txt", "r")
lines = file.readlines()
file.close()
for line in lines:
    line = line.strip()
    split_line = line.split(" ")
    valuation[split_line[0]] = list(map(int, split_line[1:32]))

stats = []
secprices = []
fixeds = []
items = [1, 1, 1, 1, 1]
winners = []


def query(buyer, price, cur_items):
    utility = [0] * 31
    for i in [0, 1, 3, 7, 15]:
        utility[i] = valuation[buyer][i] - price
    for i in [2, 4, 5, 8, 9, 11, 16, 17, 19, 23]:
        utility[i] = valuation[buyer][i] - 2 * price
    for i in [6, 10, 12, 13, 18, 20, 21, 24, 25, 27]:
        utility[i] = valuation[buyer][i] - 3 * price
    for i in [14, 22, 26, 28, 29]:
        utility[i] = valuation[buyer][i] - 4 * price
    utility[30] = valuation[buyer][i] - 5 * price
    if cur_items[0] == 0:
        utility[0] = utility[2] = utility[4] = utility[6] = -400000
        utility[8] = utility[10] = utility[12] = utility[14] = -400000
        utility[16] = utility[18] = utility[20] = utility[22] = -400000
        utility[24] = utility[26] = utility[28] = utility[30] = -400000
    if cur_items[1] == 0:
        utility[1] = utility[2] = utility[5] = utility[6] = -400000
        utility[9] = utility[10] = utility[13] = utility[14] = -400000
        utility[17] = utility[18] = utility[21] = utility[22] = -400000
        utility[25] = utility[26] = utility[29] = utility[30] = -400000
    if cur_items[2] == 0:
        utility[3] = utility[4] = utility[5] = utility[6] = -400000
        utility[11] = utility[12] = utility[13] = utility[14] = -400000
        utility[19] = utility[20] = utility[21] = utility[22] = -400000
        utility[27] = utility[28] = utility[29] = utility[30] = -400000
    if cur_items[3] == 0:
        utility[7] = utility[8] = utility[9] = utility[10] = -400000
        utility[11] = utility[12] = utility[13] = utility[14] = -400000
        utility[23] = utility[24] = utility[25] = utility[26] = -400000
        utility[27] = utility[28] = utility[29] = utility[30] = -400000
    if cur_items[4] == 0:
        utility[15] = utility[16] = utility[17] = utility[18] = -400000
        utility[19] = utility[20] = utility[21] = utility[22] = -400000
        utility[23] = utility[24] = utility[25] = utility[26] = -400000
        utility[27] = utility[28] = utility[29] = utility[30] = -400000

    index = utility.index(max(utility))
    if utility[index] < 0:
        return [[], 0]
    tmp_sw = valuation[buyer][index]
    index = index + 1
    demand = []
    j = 0

    while index:
        if index % 2 == 1:
            demand.append(j)
        j = j + 1
        index = index >> 1
    return demand, tmp_sw


def orign(m):
    tmp_items = items.copy()
    model = gp.Model()
    opt = 0
    allocation = {}
    if len(stats) != 0:
        model.setParam('OutputFlag', False)
        x = model.addVars(len(stats) * 31, lb=0, ub=1, vtype=gp.GRB.INTEGER, name='x')
        c = []
        for stat in stats:
            c.extend(valuation[stat])
        p = [[0 for i in range(len(c))] for j in range(len(stats) + m)]
        for i in range(len(stats)):
            for j in range(31):
                p[i][j + 31 * i] = 1

        for i in range(len(stats)):
            p[len(stats)][0 + i * 31] = 1
            p[len(stats)][2 + i * 31] = 1
            p[len(stats)][4 + i * 31] = 1
            p[len(stats)][6 + i * 31] = 1
            p[len(stats)][8 + i * 31] = 1
            p[len(stats)][10 + i * 31] = 1
            p[len(stats)][12 + i * 31] = 1
            p[len(stats)][14 + i * 31] = 1
            p[len(stats)][16 + i * 31] = 1
            p[len(stats)][18 + i * 31] = 1
            p[len(stats)][20 + i * 31] = 1
            p[len(stats)][22 + i * 31] = 1
            p[len(stats)][24 + i * 31] = 1
            p[len(stats)][26 + i * 31] = 1
            p[len(stats)][28 + i * 31] = 1
            p[len(stats)][30 + i * 31] = 1

        for i in range(len(stats)):
            p[len(stats) + 1][1 + i * 31] = 1
            p[len(stats) + 1][2 + i * 31] = 1
            p[len(stats) + 1][5 + i * 31] = 1
            p[len(stats) + 1][6 + i * 31] = 1
            p[len(stats) + 1][9 + i * 31] = 1
            p[len(stats) + 1][10 + i * 31] = 1
            p[len(stats) + 1][13 + i * 31] = 1
            p[len(stats) + 1][14 + i * 31] = 1
            p[len(stats) + 1][17 + i * 31] = 1
            p[len(stats) + 1][18 + i * 31] = 1
            p[len(stats) + 1][21 + i * 31] = 1
            p[len(stats) + 1][22 + i * 31] = 1
            p[len(stats) + 1][25 + i * 31] = 1
            p[len(stats) + 1][26 + i * 31] = 1
            p[len(stats) + 1][29 + i * 31] = 1
            p[len(stats) + 1][30 + i * 31] = 1

        for i in range(len(stats)):
            p[len(stats) + 2][3 + i * 31] = 1
            p[len(stats) + 2][4 + i * 31] = 1
            p[len(stats) + 2][5 + i * 31] = 1
            p[len(stats) + 2][6 + i * 31] = 1
            p[len(stats) + 2][11 + i * 31] = 1
            p[len(stats) + 2][12 + i * 31] = 1
            p[len(stats) + 2][13 + i * 31] = 1
            p[len(stats) + 2][14 + i * 31] = 1
            p[len(stats) + 2][19 + i * 31] = 1
            p[len(stats) + 2][20 + i * 31] = 1
            p[len(stats) + 2][21 + i * 31] = 1
            p[len(stats) + 2][22 + i * 31] = 1
            p[len(stats) + 2][27 + i * 31] = 1
            p[len(stats) + 2][28 + i * 31] = 1
            p[len(stats) + 2][29 + i * 31] = 1
            p[len(stats) + 2][30 + i * 31] = 1

        for i in range(len(stats)):
            p[len(stats) + 3][7 + i * 31] = 1
            p[len(stats) + 3][8 + i * 31] = 1
            p[len(stats) + 3][9 + i * 31] = 1
            p[len(stats) + 3][10 + i * 31] = 1
            p[len(stats) + 3][11 + i * 31] = 1
            p[len(stats) + 3][12 + i * 31] = 1
            p[len(stats) + 3][13 + i * 31] = 1
            p[len(stats) + 3][14 + i * 31] = 1
            p[len(stats) + 3][23 + i * 31] = 1
            p[len(stats) + 3][24 + i * 31] = 1
            p[len(stats) + 3][25 + i * 31] = 1
            p[len(stats) + 3][26 + i * 31] = 1
            p[len(stats) + 3][27 + i * 31] = 1
            p[len(stats) + 3][28 + i * 31] = 1
            p[len(stats) + 3][29 + i * 31] = 1
            p[len(stats) + 3][30 + i * 31] = 1

        for i in range(len(stats)):
            p[len(stats) + 4][15 + i * 31] = 1
            p[len(stats) + 4][16 + i * 31] = 1
            p[len(stats) + 4][17 + i * 31] = 1
            p[len(stats) + 4][18 + i * 31] = 1
            p[len(stats) + 4][19 + i * 31] = 1
            p[len(stats) + 4][20 + i * 31] = 1
            p[len(stats) + 4][21 + i * 31] = 1
            p[len(stats) + 4][22 + i * 31] = 1
            p[len(stats) + 4][23 + i * 31] = 1
            p[len(stats) + 4][24 + i * 31] = 1
            p[len(stats) + 4][25 + i * 31] = 1
            p[len(stats) + 4][26 + i * 31] = 1
            p[len(stats) + 4][27 + i * 31] = 1
            p[len(stats) + 4][28 + i * 31] = 1
            p[len(stats) + 4][29 + i * 31] = 1
            p[len(stats) + 4][30 + i * 31] = 1

        r = [1] * (len(stats) + m)
        model.update()
        model.setObjective(x.prod(c), gp.GRB.MAXIMIZE)
        model.addConstrs(x.prod(p[i]) <= r[i] for i in range(len(stats) + m))
        model.optimize()
        opt = model.objVal

    else:
        opt = 0
    reserve = opt / math.sqrt(m)
    tmp_sw = reserve
    tmp_pay = reserve
    winner = ""
    for buyer in secprices:
        if valuation[buyer][14] > reserve and valuation[buyer][6] > tmp_sw:
            winner = buyer
            tmp_pay = tmp_sw
            tmp_sw = valuation[buyer][14]

    if len(winner) != 0:
        allocation[winner] = items
        return allocation, tmp_sw, tmp_pay

    tmp_sw = 0
    price = 0.006 * opt / 8 / m
    for buyer in fixeds:
        if 1 in tmp_items:
            res = query(buyer, price, tmp_items)
            demand = res[0]
            if demand is not None:
                tmp_sw = tmp_sw + res[1]
                allocation[buyer] = demand
                for d in demand:
                    tmp_items[d] = 0
        else:
            break
    return allocation, tmp_sw, price * 5


probabilities = [0.003, 0.003, 0.994]  # stat fixed second


def classify(buyer):
    numbers = list(range(1, 4))  # 设置数字范围（此处为1-3）
    result = random.choices(numbers, probabilities)  # 根据概率分布进行随机选择
    if result[0] == 1:
        stats.append(buyer)
    if result[0] == 2:
        fixeds.append(buyer)
    if result[0] == 3:
        secprices.append(buyer)


def msn(initial):
    """
    stats.extend(['1', '2', '3', '4', '5'])
    """
    for buyer in relation[initial]:
        classify(buyer)

    while True:
        flag = True
        while flag:
            flag = False
            for buyer in stats:
                for neighbor in relation[buyer]:
                    if neighbor != initial and neighbor not in fixeds and neighbor not in stats and neighbor not in secprices:
                        classify(neighbor)
                        flag = True
        res = orign(5)
        allocation = res[0]
        price = res[1]

        flag = False
        for buyer in secprices + fixeds:
            if buyer not in allocation.keys():
                for neighbor in relation[buyer]:
                    if neighbor != initial and neighbor not in fixeds and neighbor not in stats and neighbor not in secprices:
                        classify(neighbor)
                        flag = True
        if not flag:
            return res[1], res[2]


def optimal(initial):
    for buyer in relation.keys():
        if buyer != initial:
            classify(buyer)
    return orign(5)


def firstlevel(initial):
    for buyer in relation[initial]:
        if buyer != initial:
            classify(buyer)
    return orign(5)


initials = relation.keys()
nodes = random.sample(initials, 100)

file = open("result_submodular_facebook_5.txt", "a")

for buyer in nodes:

    res = msn(buyer)
    file.write(str(res[0]) + " " + str(int(res[1])) + " ")
    stats.clear()
    secprices.clear()
    fixeds.clear()
    items = [1, 1, 1, 1, 1]
    res = optimal(buyer)
    file.write(str(res[1]) + " " + str(int(res[2])) + " ")
    stats.clear()
    secprices.clear()
    fixeds.clear()
    items = [1, 1, 1, 1, 1]
    res = firstlevel(buyer)
    file.write(str(res[1]) + " " + str(int(res[2])) + "\n")
    stats.clear()
    secprices.clear()
    fixeds.clear()
    items = [1, 1, 1, 1, 1]
    print(buyer)

