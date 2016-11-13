import sys
import operator
import common
import time

def sort_transactions(transactions, sortCommonGoodsSet):

    sortTransactionSet = []
    sizeOfSortCommonGoodsSet = len(sortCommonGoodsSet)
    # sort all transactions
    for transaction in transactions:
        sortTransaction = []
        lenTransaction = len(transaction)
        # add goods in sorted order if they are in transaction
        for i in range(sizeOfSortCommonGoodsSet):
            good = list(sortCommonGoodsSet[i][0])[0]
            if lenTransaction > good and transaction[good] > 0:
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

def build_fp_tree(tree, sortTransactions):

    for transaction in sortTransactions:
        treeElement = tree.root
        # loop for each good in transaction
        for good in transaction:
            flag = False

            # check children of tree element to find node with needed name
            for child in treeElement.children:
                # if needed node is found, change it's index and set current tree element = child
                if good == child.name:
                    tree.goodSupport[tuple([good])] += 1
                    child.index += 1
                    treeElement = child
                    flag = True
                    break

            # if current tree element don't have child with needed name, add new node
            if not flag:
                newNode = tree.insert(treeElement, good)
                tree.arrayOfGoodNodes[good].append(newNode)
                treeElement = newNode
                tree.goodSupport[tuple([good])] += 1
                treeElement.index += 1

    return

def build_nominal_tree(tree, good):
    nominalTree = Tree(tree.goods)
    allPaths = []
    nodeSupport = []

    # find all paths from root to specific good
    for node in tree.arrayOfGoodNodes[good]:
        path = []
        treeElement = node
        nodeSupport.append(node.index)
        # get path from node to root
        while treeElement.name != -1:
            path.append(treeElement.name)
            treeElement = treeElement.parent
        # reverse path and add to common array
        path.reverse()
        allPaths.append(path)

    # build fp-tree based on founded paths
    build_fp_tree(nominalTree, allPaths)
    counter = 0
    # loop for all good nodes in nominal tree
    for node in nominalTree.arrayOfGoodNodes[good]:
        treeElement = node
        # remove good node from nominal fp-tree
        treeElement.children = []
        # use good support from original fp-tree for updating indexes
        while treeElement.name != -1:
            treeElement.index += nodeSupport[counter] - 1
            nominalTree.goodSupport[tuple([treeElement.name])] += nodeSupport[counter] - 1
            treeElement = treeElement.parent
        counter += 1

    return nominalTree

def find_common_sets(tree, set, commonSets, sizeOfCommonSet, commonGoods, numCurrentGood, minSupport, numTransactions):

    while numCurrentGood >= 0:
        currentGood = list(commonGoods[numCurrentGood][0])[0]
        numCurrentGood -= 1

        # if currentGood is not in tree, continue
        if not tree.goodSupport[tuple([currentGood])]:
            continue
        support = tree.goodSupport[tuple([currentGood])] / float(numTransactions)

        # add common set only if it's support is greater than minSupport
        if support >= minSupport:
            newSet = []
            sizeOfSet = len(set)
            # make new set by adding current good to previous set
            for i in range(sizeOfSet):
                newSet.append(set[i])
            newSet.append(currentGood)
            if len(commonSets) < sizeOfSet + 1:
                commonSets.append(dict())
            commonSets[sizeOfCommonSet][tuple(newSet)] = support

            # build nominal fp-tree for current good and run find_common_set for new set
            nominalTree = build_nominal_tree(tree, currentGood)
            find_common_sets(nominalTree, newSet, commonSets, sizeOfCommonSet + 1, commonGoods,
                             numCurrentGood, minSupport, numTransactions)

    return True

def run_fpgrowth(commonGoodsSet, data, numGoods, numTransactions, minSupport):
    # sort goods based on support and sort all transactions
    sortCommonGoodsSet = sorted(commonGoodsSet.items(), key=operator.itemgetter(1), reverse=True)
    sortData = sort_transactions(data, sortCommonGoodsSet)
    sizeSortCommonGoodsSet = len(sortCommonGoodsSet)

    # build fp-tree using sorted transactions
    fpTree = Tree(numGoods)
    build_fp_tree(fpTree, sortData)

    # find all common sets with support greater than minSupport
    arrayOfCommonSets = []
    find_common_sets(fpTree, [], arrayOfCommonSets, 0, sortCommonGoodsSet, sizeSortCommonGoodsSet - 1,
                     minSupport, numTransactions)

    return arrayOfCommonSets

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

    # read transactions from csv file
    data = common.get_dataset_from_csv_file(dataFileName)
    numTransactions = len(data)
    numGoods = 0
    if data:
        numGoods = len(data[0])

    # count support of each good
    commonGoodsSet = dict()
    common.count_good_support(data, numTransactions, commonGoodsSet, numGoods)
    for i in range(numGoods):
        if commonGoodsSet[tuple([i])] < minSupport:
            del commonGoodsSet[tuple([i])]

    # run fp-growth algorithm for finding common sets
    arrayOfCommonSets = run_fpgrowth(commonGoodsSet, data, numGoods, numTransactions, minSupport)

    # find common rules from common sets (confidence more than minConf)
    commonRules = dict()
    numCommonSets = len(arrayOfCommonSets)
    for i in range(1, numCommonSets):
        commonSetItems = arrayOfCommonSets[i].items()
        for key, value in commonSetItems:
            common.get_common_rules(commonRules, arrayOfCommonSets, list(key), value, minConf, list(key))

    endTime = time.time()

    # print results
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