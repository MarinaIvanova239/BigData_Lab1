import sys
import operator
import common
import time

def sort_transactions(transactions, sortCommonGoodsSet):

    sortTransactionSet = []
    sizeOfSortCommonGoodsSet = len(sortCommonGoodsSet)
    for transaction in transactions:
        sortTransaction = []
        lenTransaction = len(transaction)
        for i in range(sizeOfSortCommonGoodsSet):
            good = list(sortCommonGoodsSet[i][0])[0]
            if lenTransaction >= good and transaction[good] > 0:
                sortTransaction.append(good)

        sortTransactionSet.append(sortTransaction)

    return sortTransactionSet

class node:
    def __init__(self, name=0, parent=None, index=0):
        self.index = index
        self.name = name
        self.parent = parent
        self.children = []

class Tree:
    def __init__(self, goods=0):
        self.root = node(-1)
        self.goodSupport = dict()
        self.goods = goods
        self.arrayOfGoodNodes = []

        for i in range(goods):
            self.arrayOfGoodNodes.append([])
            self.goodSupport[tuple([i])] = 0

    def insert(self, parent, name):
        temp = node(name, parent)
        parent.children.append(temp)
        return temp

def build_fp_tree(tree, sortTransactions, numTransactions):

    for transaction in sortTransactions:
        treeElement = tree.root
        for good in transaction:
            flag = False
            for child in treeElement.children:
                if good == child.name:
                    tree.goodSupport[tuple([good])] += 1 / float(numTransactions)
                    child.index += 1 / float(numTransactions)
                    treeElement = child
                    flag = True
                    break

            if not flag:
                newNode = tree.insert(treeElement, good)
                tree.arrayOfGoodNodes[good].append(newNode)
                treeElement = newNode
                tree.goodSupport[tuple([good])] += 1 / float(numTransactions)
                treeElement.index += 1 / float(numTransactions)

    return

def build_nominal_tree(tree, good):
    nominalTree = Tree(tree.goods)
    for node in tree.arrayOfGoodNodes[good]:
        treeElement = node
        while treeElement.parent.name != -1:

            treeElement = treeElement.parent

    return nominalTree

def find_common_sets(tree, set, commonSets, sizeOfCommonSet, commonGoods, numCurrentGood, minSupport):

    while numCurrentGood >= 0:
        currentGood = list(commonGoods[numCurrentGood][0])[0]
        numCurrentGood -= 1

        if not tree.goodSupport[tuple([currentGood])]:
            continue
        support = tree.goodSupport[tuple([currentGood])]

        if support >= minSupport:
            newSet = []
            sizeOfSet = len(set)
            for i in range(sizeOfSet):
                newSet.append(set[i])
            newSet.append(currentGood)
            if (sizeOfSet == sizeOfCommonSet):
                commonSets.append(dict())
            commonSets[sizeOfCommonSet][tuple(newSet)] = support

            nominalTree = build_nominal_tree(tree, currentGood)
            find_common_sets(nominalTree, newSet, commonSets, sizeOfCommonSet + 1, commonGoods, numCurrentGood, minSupport)

    return True

if __name__ == "__main__":

    startTime = time.time()

    dataFileName = sys.argv[1]
    minSupport = float(sys.argv[2])
    minConf = float(sys.argv[3])

    if minSupport > 1 or minSupport < 0:
        print 'MinSupport must be in [0, 1]'
        quit()
    if minConf > 1 or minConf < 0:
        print 'MinConf must be in [0, 1]'
        quit()

    data = common.get_dataset_from_csv_file(dataFileName)
    numTransactions = len(data)
    numGoods = 0
    if data:
        numGoods = len(data[0])

    commonGoodsSet = dict()
    for i in range(numGoods):
        support = common.count_good_support(i, data, numTransactions)
        if support >= minSupport:
            commonGoodsSet[tuple([i])] = support

    sortCommonGoodsSet = sorted(commonGoodsSet.items(), key=operator.itemgetter(1), reverse=True)
    sortData = sort_transactions(data, sortCommonGoodsSet)
    sizeSortCommonGoodsSet = len(sortCommonGoodsSet)

    fpTree = Tree(numGoods)
    build_fp_tree(fpTree, sortData, numTransactions)

    arrayOfCommonSets = []
    find_common_sets(fpTree, [], arrayOfCommonSets, 0, sortCommonGoodsSet, sizeSortCommonGoodsSet - 1, minSupport)

    commonRules = dict()
    numCommonSets = len(arrayOfCommonSets)
    for i in range(1, numCommonSets):
        commonSetItems = arrayOfCommonSets[i].items()
        for key, value in commonSetItems:
            common.get_common_rules(commonRules, arrayOfCommonSets, list(key), value, minConf, list(key))

    endTime = time.time()

    print 'items:'
    for commonSet in arrayOfCommonSets:
        for element, support in commonSet.items():
            print element, ':', support

    print '.......'
    print 'rules:'
    for eachRule, conf in commonRules.items():
        print eachRule, ':', conf

    print '.......'
    print 'time=', endTime - startTime