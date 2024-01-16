import random
import math

file = open("email.txt", "r")
lines = file.readlines()
file.close()
relation = {}
valuation = {}
bundle = {}
number = 30

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


def generate(m):
    array = list(range(1, m + 1))
    for buyer in relation.keys():
        valuation[buyer] = random.randint(1, 200000)
        bundle[buyer] = set(random.sample(array, random.randint(1, int(m/2))))


def orign(buyers, items, removed):
    values = []
    allocation = {}
    for buyer in buyers:
        values.append((buyer, valuation[buyer]))
    values = sorted(values, key=lambda t: t[1], reverse=True)
    if len(removed) > 0:
        values.remove((removed, valuation[removed]))
    for buyer in values:
        if len(items) == 0:
            break;
        if bundle[buyer[0]].issubset(items):
            items = items - bundle[buyer[0]]
            allocation[buyer[0]] = bundle[buyer[0]]
    return allocation


def gda(initial, m):
    items = set(range(1, m + 1))
    accessible = []
    for buyer in relation[initial]:
        accessible.append(buyer)
    tmp_items = items.copy()
    active = accessible.copy()
    sw = 0
    revenue = 0
    winners = []
    while len(items):
        flag = True
        while flag:
            tmp_items = items.copy()
            allocation = orign(active, tmp_items, "")
            pw = allocation.keys()
            flag = False
            for buyer in active:
                if buyer not in pw:
                    active.remove(buyer)
                    flag = True
                    for neighbour in relation[buyer]:
                        if neighbour not in accessible and neighbour not in winners and neighbour != initial:
                            active.append(neighbour)
                            accessible.append(neighbour)

        for w in pw:
            sw = sw + len(allocation[w]) * valuation[w]
            tmp_items = items.copy()
            tmp_all = orign(accessible, tmp_items, w)
            pay = 0
            for key in tmp_all.keys():
                if len(bundle[key].intersection(bundle[w])) != 0 and valuation[key] > pay:
                    pay = valuation[key]
            revenue = revenue + pay * len(allocation[w])

        winners.extend(pw)
        for w in pw:
            active.remove(w)
            accessible.remove(w)
            for neighbour in relation[w]:
                if neighbour not in accessible and neighbour not in winners and neighbour != initial:
                    active.append(neighbour)
                    accessible.append(neighbour)
            items = items - bundle[w]
        if not flag and len(allocation) == 0:
            break
    return sw,revenue

def igda(initial, m):
    items = set(range(1, m + 1))
    accessible = []
    for buyer in relation[initial]:
        accessible.append(buyer)
    tmp_items = items.copy()
    active = accessible.copy()
    sw = 0
    revenue = 0
    winners = []
    while len(items) > 0:
        flag = True
        while flag:
            tmp_items = items.copy()
            allocation = orign(active, tmp_items, "")
            pw = allocation.keys()
            flag = False
            for buyer in active:
                if buyer not in pw:
                    active.remove(buyer)
                    flag = True
                    for neighbour in relation[buyer]:
                        if neighbour not in accessible and neighbour not in winners and neighbour != initial:
                            active.append(neighbour)
                            accessible.append(neighbour)

        max = -1
        winner = ""
        for w in pw:
            if len(relation[w]) > max:
                winner = w
                max = len(relation[w])

        sw = sw + len(allocation[winner]) * valuation[winner]
        tmp_items = items.copy()
        tmp_all = orign(accessible, tmp_items, winner)
        pay = 0
        for key in tmp_all.keys():
            if len(bundle[key].intersection(bundle[winner])) != 0 and valuation[key] > pay:
                pay = valuation[key]
        revenue = revenue + pay * len(allocation[winner])
        winners.append(winner)
        active.remove(winner)
        accessible.remove(winner)
        for neighbour in relation[winner]:
            if neighbour not in accessible and neighbour not in winners and neighbour != initial:
                active.append(neighbour)
                accessible.append(neighbour)
        items = items - bundle[winner]
        if not flag and len(allocation) == 0:
            break
    return sw,revenue

def layer(initial, m):
    items = set(range(1, m + 1))
    accessible = relation[initial]
    tmp_items = items.copy()
    allocation = orign(accessible, tmp_items, "")
    pw = allocation.keys()
    sw = 0
    revenue = 0
    for w in pw:
        sw = sw + len(allocation[w]) * valuation[w]
        tmp_items = items.copy()
        tmp_all = orign(accessible, tmp_items, w)
        pay = 0
        for key in tmp_all.keys():
            if len(bundle[key].intersection(bundle[w])) != 0 and valuation[key] > pay:
                pay = valuation[key]
        revenue = revenue + pay * len(allocation[w])
    return sw, revenue

def optimal(initial, m):
    items = set(range(1, m + 1))
    accessible = list(relation.keys())
    accessible.remove(initial)
    tmp_items = items.copy()
    allocation = orign(accessible, tmp_items,"")
    pw = allocation.keys()
    sw = 0
    revenue=0
    for w in pw:
        sw = sw + len(allocation[w]) * valuation[w]
        tmp_items = items.copy()
        tmp_all = orign(accessible, tmp_items, w)
        pay = 0
        for key in tmp_all.keys():
            if len(bundle[key].intersection(bundle[w])) != 0 and valuation[key] > pay:
                pay = valuation[key]
        revenue = revenue + pay * len(allocation[w])
    return sw,revenue


'''
file = open("value_case4_facebook.txt", "w")
generate(20)

for key in relation.keys():
    file.write(key+" "+str(valuation[key])+'\n')
'''

generate(number)

initials = list(relation.keys())
nodes = random.sample(initials, 100)

file = open("result_singleminded_email_"+str(number)+".txt", "w")


for buyer in nodes:
    print(buyer)
    try:
        r1 = gda(buyer, number)
        r2 = igda(buyer, number)
        r3 = optimal(buyer, number)
        r4 = layer(buyer,number)
        file.write(str(r1[0])+" "+str(r2[0])+" "+str(r3[0])+" "+str(r4[0])+" "
                   +str(r1[1])+" "+str(r2[1])+" "+str(r3[1])+" "+str(r4[1])+"\n")
    except:
        print(buyer + "!!!!!!!!")

