import re
import csv

def load_Groceries(filename):
    dataset = []
    #使用open函数打开文件
    with open(filename)as f:
        #读出文件内容
        f_csv = csv.reader(f)
        #enumerate枚举函数,返回标签index和元素value
        for index, value in enumerate(f_csv):
            if index != 0:
                #按照','分割
                goodsList = str(value[1]).split(',')
                dataset.append(list(goodsList))
    return dataset

def C_sup(dataset,itemset_Ck):
    C_sup = []
    for c in itemset_Ck:
        count = 0  #计数
        for i in range(len(dataset)):
            if set(c) <= set(dataset[i]):  #选择不重复的元素
                count += 1
        C_sup.append([c,count])
    return C_sup

'''
二进制法枚举所有子集
输入：列表items
输出：需要调用之后循环输出,列表形式
4 >> 1 = 2  ,4 >> 2 = 1(因为4=100，1向右移动1位得到010=2，向右移动2位得到001=1)
'''
def PowerSetsBinary(items):
    #生成n个元素items的所有组合
    n = len(items)
    #枚举2**n个可能的组合(n个元素的集合的子集有2**n个)
    for i in range(2**n):
        subset = []  #存放子集
        #j控制要选取的元素当前的下标对应的值
        for j in range(n):
            #i >> j 指i在二进制的形式将1向右移动j位
            #向右移动j次,判断结果除以2 余1 来得到是否要取当前的下标对应的值
            if(i >> j ) % 2 == 1:
                subset.append(items[j])
        #呼叫subset
        yield subset


'''
最大频繁项集的元素，不为别的频繁项集的子集
输入：频繁项目集L
输出：最大频繁项集Lmax
'''
def max_frequentSet(L):
    L = L[1:]  # 因为要考虑的是关联规则，频繁1项集生成的规则不是就关联规则，故不考虑
    Lmax = []  # 存放最大频繁项集
    # 对于每组频繁k-1项集，频繁k项集不考虑，因为其肯定为最大频繁项集
    for i in range(len(L) - 1):
        L_compared = []  # 存放要被拿来比较是否为子集的元素
        for j in range(i + 1, len(L)):
            for k in range(len(L[j])):
                L_compared.append(L[j][k])
        # 开始比较
        for j in range(len(L[i])):
            count = 0  # 统计L_compared中元素不包含L[i][j]的个数
            for k in range(len(L_compared)):
                if set(L[i][j]) < set(L_compared[k]):  # 如果是子集，直接结束在L_compared中的比较
                    break
                else:
                    count += 1  # 不是子集，则次数加一
            # 如果L_compared中元素不包含L[i][j]的个数和L_compared的个数相等，则可以认为L[i][j]不是L_compared的子集
            if count == len(L_compared):
                Lmax.append(L[i][j])

    # 将频繁k项集加入最大频繁项集
    for i in range(len(L[-1])):
        Lmax.append(L[-1][i])

    return Lmax

'''
输入：一个候选k项集c，格式为[2, 3, 5]
      频繁k-1项集，格式为[[1,3],[2,3],[2,5],[3,5]]
输出：c是否从候选集中删除的布尔判断
      返回True删除
      返回False不删除
'''
def has_infrequent_subset(c,Lkn):
    #调用函数PowerSetsBinary(c)
    for subset in PowerSetsBinary(c):
        #只考虑k-1个元素的子集
        if len(subset) == len(Lkn[0]):
            if subset not in Lkn:
                return True
    return False


'''
输入：频繁(k-1)项集Lkn，格式为[[1],[2],[3],[5]]
输出：候选k项集Ck，格式为
'''
def apriori_gen(Lkn):
    Ck = []  # 存放候选k项集
    # 遍历频繁k-1项集的每一个元素
    for i in range(len(Lkn)):
        p = Lkn[i]
        # 遍历频繁k-1项集在p之后的每个元素
        for j in range(i + 1, len(Lkn)):
            q = Lkn[j]

            count = 0  # 计算相等元素的个数
            for k in range(len(p) - 1):
                if p[k] == q[k]:
                    count += 1

            c = []  # 存放可以合并的元素
            if count == len(p) - 1:
                if p[count] < q[count]:  # 如果p最后一个元素<q最后一个元素
                    c = p.copy()  # c.append(p)
                    c.append(q[count])  # 将q的第k-1个(最后一个)元素加到p中并赋给c（c=p∞q）

            # 若c非空，则判断c是否为频繁项目集的候选元素
            if c != []:
                if has_infrequent_subset(c, Lkn) == False:
                    Ck.append(c)
    return Ck


'''
输入：数据集dataset
      最小支持率minsupport,为小数，例如0.5
输出：最大频繁项目集Lmax
'''


def Apriori(dataset, minsupport):
    # 计算最小支持数
    minsup_count = len(dataset) * minsupport

    # 候选1项集C1
    C1 = []
    C1_set = set()  # 因为候选集中元素不能重复，用集合是最方便的
    for i in range(len(dataset)):
        data = set(dataset[i])
        C1_set.update(data)  # 取两个集合的并集
    # 将集合中元素依次转换成列表形式，加入到大列表C1中
    # e.g.C1 = [[1], [2], [3], [4], [5]]
    for i in range(len(list(C1_set))):
        C1.append([list(C1_set)[i]])
    # print(C1)

    # 计算候选1项集的sup，调用自编函数C_sup(dataset,itemset_Ck)
    C1_sup = C_sup(dataset, C1)
    # print(C1_sup)

    # 频繁1项集L1
    L1 = []
    for item in C1_sup:
        if item[1] >= minsup_count:
            L1.append(item[0])
    # print(L1)

    L = []  # 存放频繁项目集
    L.append(L1)

    # 求接下来的频繁k项集
    Lkn = L1.copy()  # 频繁k-1项集
    while True:
        # 调用自编函数apriori_gen(Lkn)获得k个元素的候选集
        Ck = apriori_gen(Lkn)
        if Ck != []:
            # 计算候选k项集的sup，调用自编函数C_sup(dataset,itemset_Ck)
            Ck_sup = C_sup(dataset, Ck)
            # print(Ck_sup)

            # 得到所有支持数不小于minsup_count的频繁k项集Lkn
            Lkn = []  # 存放频繁k项集
            for item in Ck_sup:
                if item[1] >= minsup_count:
                    Lkn.append(item[0])

            L.append(Lkn)
        else:  # 候选k项集Ck为空则频繁k项集为空，故结束循环
            break

    print('频繁项集为：', L)

    if L != [[]]:
        # 调用自编函数max_frequentSet(L)求出最大频繁项集
        Lmax = max_frequentSet(L)
        return Lmax
    else:
        return []


'''
输入：最大频繁项集Lmax，格式为[[1, 3],[2, 3, 5]]
      最小置信度minconf，格式为小数(e.g.0.8)
输出：关联规则
'''


def Rule_generate(dataset, Lmax, minconf):
    rules = []
    # 遍历所有最大频繁项目集
    for l_k in Lmax:
        # 递归调用genrules函数
        rule = genrules(dataset, l_k, l_k)
        rules.append(rule)

    finalRules = []
    # 去除重复项
    for rule in rules:
        finalRules.append(list(set(rule)))

    return finalRules


'''
输入：l_k频繁k项集，格式为[2,3,5]
      x_m频繁m项集
输出：关联规则
'''
def genrules(dataset, l_k, x_m):
    # 求出x_m的含有m-1项的子集
    m = len(x_m)

    rules = []
    # 调用自编函数PowerSetsBinary得到x_m的所有子集s
    for s in PowerSetsBinary(x_m):
        # 找出含有m-1项的子集
        if len(s) == m - 1:
            # 调用自编函数C_sup计算支持数
            l_k_sup = C_sup(dataset, [l_k])
            s_sup = C_sup(dataset, [s])
            # 计算置信度（因为 C_sup函数输出格式的原因，sup值在a[0][1])
            conf = l_k_sup[0][1] / s_sup[0][1]
            # l_k - x_(m-1)得到的元素
            other = [l_k[i] for i in range(len(l_k)) if l_k[i] not in s]
            # 计算l_k的支持率
            support = l_k_sup[0][1] / len(dataset)
            print('l_k:{0}, x_m-1:{1}'.format(l_k, s))

            # 判断规则是否是强关联规则
            if conf >= minconf:  # 是强关联规则                                            round(a,2)是保留a小数点后两位有效数字
                rule = '规则 {0} => {1}, support={2}, confidence={3},({4})强关联规则'.format(s, other, round(support, 2),
                                                                                      round(conf, 2), '是')
            else:  # 不是强关联规则
                rule = '规则 {0} => {1}, support={2}, confidence={3},({4})强关联规则'.format(s, other, round(support, 2),
                                                                                      round(conf, 2), '不是')
            rules.append(rule)
            print(rule)
            print('\n')

            # 若x_(m-1)中元素个数大于1（因为小等于1个元素就无法生成关联规则）
            if m - 1 > 1:
                # 递归调用genrules函数
                rule = genrules(dataset, l_k, s)
                # 拉平了放入rules中
                for i in range(len(rule)):
                    rules.append(rule[i])

    return rules


'''
输入：rules是之前得到的规则列表
输出：替换好商品名称的规则列表
'''

def Replace_goodsname(rules):
    finalRules = []
    # 调用re函数库中的complie函数设置一个查找的模式
    # \d为0~9的数字
    # +表示无论多少位
    pattern = re.compile(r'\d+')

    # 遍历规则rules准备替换
    for rule in rules:
        # 调用re函数库中的findall函数，可以按照自己定义的模式寻找所有符合条件的字符串，返回一个列表
        ruleNum = findall
        # 序列解包，按照','分割，rest是除了前面以外剩下的
        ruleList, *rest = rule[0].split(',')
        # 得到新的规则
        ruleNew = '规则 [%s] => [%s]' % (list(goodlist)[int(ruleNum[0])], list(goodlist)[int(ruleNum[1])])
        print(ruleNew)
        for other in rest:
            ruleNew = ruleNew + ',' + other
        finalRules.append(ruleNew)
    return finalRules
