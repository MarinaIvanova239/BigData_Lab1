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
    def __init__(self, name=0, parent=None):
        self.index = 0
        self.name = name
        self.children = []
        self.parent = parent

class Tree:
    def __init__(self, transactions=0, goods=0):
        self.root = node(-1)
        self.transactions = transactions
        self.goodSupport = dict()
        self.goods = goods
        self.arrayOfGoodNodes = []

        for i in range(numGoods):
            self.arrayOfGoodNodes.append([])
            self.goodSupport[tuple([i])] = 0

    def insert(self, parent, name):
        temp = node(name, parent)
        parent.children.append(temp)
        return temp

def build_fp_tree(tree, sortTransactions, numTransactions, startSupport):

    counter = 0
    for transaction in sortTransactions:
        treeElement = tree.root
        for good in transaction:
            flag = False
            for child in treeElement.children:
                if good == child.name:
                    if startSupport:
                        tree.goodSupport[tuple([good])] += startSupport[counter]
                        child.index += startSupport[counter]
                    else:
                        tree.goodSupport[tuple([good])] += 1 / float(numTransactions)
                        child.index += 1 / float(numTransactions)
                    treeElement = child
                    flag = True
                    break

            if not flag:
                newNode = tree.insert(treeElement, good)
                tree.arrayOfGoodNodes[good].append(newNode)
                treeElement = newNode
                if startSupport:
                    tree.goodSupport[tuple([good])] += startSupport[counter]
                    treeElement.index += startSupport[counter]
                else:
                    tree.goodSupport[tuple([good])] += 1 / float(numTransactions)
                    treeElement.index += 1 / float(numTransactions)

        counter += 1

    return

def find_paths(good, treeElement, path, paths, pathsSupport):

    if treeElement.name == good and path != []:
        paths.append(path)
        pathsSupport.append(treeElement.index)
        return True

    if treeElement.name != -1:
        path.append(treeElement.name)

    originalPath = tuple(path)
    for child in treeElement.children:
        find_paths(good, child, list(originalPath), paths, pathsSupport)

    return True

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
            paths = []
            pathsSupport = []
            find_paths(currentGood, tree.root, [], paths, pathsSupport)
            nominalTree = Tree(tree.transactions, tree.goods)
            build_fp_tree(nominalTree, paths, tree.transactions, pathsSupport)
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

    fpTree = Tree(numTransactions, numGoods)
    build_fp_tree(fpTree, sortData, numTransactions, [])

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