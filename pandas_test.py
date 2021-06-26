import pandas as pd

test_list = ['괴물', '오컬트']
file1 = pd.read_csv("/Users/seolyumin/Hackathon-selenium/통합 문서1.csv", header=None, names=["title", "rate", "plot"])
title = list(file1['title'])
rate = list(file1['rate'])
plot = list(file1['plot'])
print(title)
print(rate)
print(plot)
'''
for k in test_list:
    if k in plot:
        print()
'''

[print(title[plot.index(i)]) for i in plot if '괴물' in i]

