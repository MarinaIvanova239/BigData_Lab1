import sys
import operator
import common
import time

def sort_transactions(transactions, sortCommonGoodsSet):

    sortTransactionSet = []
    sizeOfSortCommonGoodsSet = len(sortCommonGoodsSet)
    for transaction in transactions:
        sortTransaction = []
        for i in range(sizeOfSortCommonGoodsSet):
            good = list(sortCommonGoodsSet[i][0])[0]
            if transaction[good] > 0:
                sortTransaction.append(good)

        sortTransactionSet.append(sortTransaction)

    return sortTransactionSet

class node:
    def __init__(self, name=0, transactions=0):
        self.index = 1 / float(transactions)
        self.name = name
        self.children = []

class Tree:
    def __init__(self, transactions=0):
        self.root = node(-1, transactions)
        self.transactions = transactions
        self.goodSupport = dict()

    def insert(self, parent, name):
        temp = node(name, self.transactions)
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
                treeElement = newNode
                if not tree.goodSupport.has_key(tuple([good])):
                    tree.goodSupport[tuple([good])] = 0
                else:
                    tree.goodSupport[tuple([good])] += 1 / float(numTransactions)


def find_common_sets(tree, set, commonSets, commonGoods, numCurrentGood, minSupport):

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
            commonSets[tuple(newSet)] = support
            #nominalTree = build_nominal_tree()
            find_common_sets(nominalTree, newSet, commonSets, commonGoods, numCurrentGood, minSupport)

    return True

if __name__ == "__main__":

    startTime = time.time()

    dataFileName = sys.argv[1]
    minSupport = float(sys.argv[2])
    minConf = float(sys.argv[3])

    data = common.parse_csv_dataset(dataFileName)
    numTransactions = len(data)
    numGoods = len(data[0])

    arrayOfCommonSets = []
    commonGoodsSet = dict()
    for i in range(numGoods):
        support = common.count_good_support(i, data, numTransactions)
        if support >= minSupport:
            commonGoodsSet[tuple([i])] = support

    sortCommonGoodsSet = sorted(commonGoodsSet.items(), key=operator.itemgetter(1), reverse=True)
    sortData = sort_transactions(data, sortCommonGoodsSet)
    sizeSortCommonGoodsSet = len(sortCommonGoodsSet)

    fpTree = Tree(numTransactions)
    build_fp_tree(fpTree, sortData, numTransactions)

    arrayOfCommonSets = dict()
    find_common_sets(fpTree, [], arrayOfCommonSets, sortCommonGoodsSet, sizeSortCommonGoodsSet - 1, minSupport)

    endTime = time.time()

    print 'items:'
    for commonSet, support in arrayOfCommonSets.items():
        print commonSet, ':', support

    #print '.......'
    #print 'rules:'
    #for eachRule, conf in commonRules.items():
    #    print eachRule, ':', conf

    print '.......'
    print 'time=', endTime - startTime