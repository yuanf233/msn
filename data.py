file = open("result_subadditive_email_5.txt", "r")
lines = file.readlines()
file.close()
sw_msn = []
sw_opt = []
sw_layer = []
re_msn = []
re_opt = []
re_layer = []

m = 10
items = 1

for line in lines:
    line = line.strip()
    split_line = line.split(" ")
    sw_msn.append(int(split_line[0]))
    sw_opt.append(int(split_line[2]))
    sw_layer.append(int(split_line[4]))
    re_msn.append(int(split_line[1]))
    re_opt.append(int(split_line[3]))
    re_layer.append(int(split_line[5]))

sum_msn = int(sum(sw_msn[0:m]) / m / items)
sum_opt = int(sum(sw_opt[0:m]) / m / items)
sum_layer = int(sum(sw_layer[0:m]) / m / items)
sum_re_msn = int(sum(re_msn[0:m]) / m / items)
sum_re_opt = int(sum(re_opt[0:m]) / m / items)
sum_re_layer = int(sum(re_layer[0:m]) / m / items)

print(sum_msn, sum_opt, sum_layer, sum_re_msn, sum_re_opt, sum_re_layer)

'''1293955 1179801 1529933 435485 472441 1202547        0.02'''
'''1530197 1598514 1471303 1279471 1328108 1134419      0.01'''
'''1690154 1714094 1562714 1528985 1614176 1264242      0.005'''
'''1752989 1800850 1491055 1667293 1793300 1174364      0.002'''
