import pandas as pd
from Apriori import *

filename = r'C:\Users\LENOVO\Desktop\Groceries.csv'
Groceries = load_Groceries(filename)
Groceries

good = Groceries[0]
for i in range(1,len(Groceries)):
    for j in range(len(Groceries[i])):
        good.append(Groceries[i][j])
#用集合的形式将重复元素去掉
goodlist = set(good)
goodlist

#按顺序得到商品编号
goodnum = [k for k in range(len(goodlist))]

#将Groceries数据集中的商品名称换成商品标号
dataset = []
for i in range(len(Groceries)):
    #list形式不能使用replace函数,Series和str才行
    data = pd.Series(Groceries[i])
    data.replace(list(goodlist),goodnum,inplace=True)
    dataset.append(list(data))


data = pd.Series(Groceries[0])
#计算数据中不同元素以及其出现的次数
data_count = data.value_counts()
for k,v in dict(data_count).items():
    #找出所有support>=0.1的商品
    if v >= len(Groceries)*0.1:
        print(k)

#设置minsupport = 0.03
minsupport =  0.03
Lmax = Apriori(dataset,minsupport)

#设置最小置信度
minconf = 0.25

rules = Rule_generate(dataset,Lmax,minconf)
finalRules = Replace_goodsname(rules)
