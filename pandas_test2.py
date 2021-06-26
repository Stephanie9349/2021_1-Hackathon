import pandas as pd

test_list = ['폐쇄', '산사태', '해일', '가족'] # 자연재해 -> 폐쇄, 산사태, 해일, 가족
list_flag = [0 for i in range(len(test_list))]
flag_num = [0 for i in range(len(test_list))]
file1 = pd.read_csv("/Users/seolyumin/Hackathon-selenium/csv_test2.csv", header=None, names=["title", "rate", "plot"])
title = list(file1['title'])
rate = list(file1['rate'])
plot = list(file1['plot'])
priority = [0 for i in range(len(title))]
priority_index = [0 for i in range(len(priority))]

for k in test_list:
    for i in plot:
        if k in i:
            list_flag[test_list.index(k)] = 1
            priority[plot.index(i)] += 1

flag_num = priority[:]

for i in range(len(priority)):
    priority_index[i] = priority.index(max(priority))
    priority[priority.index(max(priority))] = -1

for i in range(len(priority_index)):
    if flag_num[priority_index[i]] > 0:
        print(title[priority_index[i]], "# 키워드", flag_num[priority_index[i]], "개 포함 |", "당신과의 찰떡 지수:", flag_num[priority_index[i]] / len(test_list) * 100, "%")
