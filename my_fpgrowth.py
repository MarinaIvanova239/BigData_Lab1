import sys
import operator
import common

def sort_transactions(transactions, sortCommonGoodsSet):

    sortTransactionSet = []
    sizeOfSortCommonGoodsSet = len(sortCommonGoodsSet)
    for eachTransction in transactions:
        sortTransaction = []
        for i in range(sizeOfSortCommonGoodsSet):
            good = list(sortCommonGoodsSet[i][0])[0]
            if eachTransction[good] > 0:
                sortTransaction.append(good)

        sortTransactionSet.append(sortTransaction)

    return sortTransactionSet

class node:
    def __init__(self, name=0):
        self.index = 1
        self.name = name
        self.child = []

class Tree:
    def __init__(self):
        self.root = node(-1)

    def insert(self, parent, name):
        temp = node(name)
        parent.child.append(temp)
        return temp

def build_fp_tree(tree, sortTransactions):

    for eachTransaction in sortTransactions:
        treeElement = tree.root
        for eachElement in eachTransaction:
            flag = False
            for child in treeElement.child:
                if eachElement == child.name:
                    child.index += 1
                    treeElement = child
                    flag = True
                    break

            if not flag:
                newNode = tree.insert(treeElement, eachElement)
                treeElement = newNode

if __name__ == "__main__":

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
        if support > minSupport:
            commonGoodsSet[tuple([i])] = support

    sortCommonGoodsSet = sorted(commonGoodsSet.items(), key=operator.itemgetter(1), reverse=True)
    sortData = sort_transactions(data, sortCommonGoodsSet)

    fpTree = Tree()
    build_fp_tree(fpTree, sortData)




