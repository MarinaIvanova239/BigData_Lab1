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
        self.children = []

class Tree:
    def __init__(self):
        self.root = node(-1)

    def insert(self, parent, name):
        temp = node(name)
        parent.children.append(temp)
        return temp

def build_fp_tree(tree, sortTransactions):

    for eachTransaction in sortTransactions:
        treeElement = tree.root
        for eachElement in eachTransaction:
            flag = False
            for child in treeElement.children:
                if eachElement == child.name:
                    child.index += 1
                    treeElement = child
                    flag = True
                    break

            if not flag:
                newNode = tree.insert(treeElement, eachElement)
                treeElement = newNode


def find_paths(good, treeElement, path, pathSupport, pathArray):

    if treeElement.name == good and path != []:
        pathArray[(tuple(path), tuple(pathSupport))] = treeElement.index
        return True

    if treeElement.name != -1:
        path.append(treeElement.name)
        pathSupport.append(treeElement.index)

    originalPath = tuple(path)
    originalPathSupport = tuple(pathSupport)
    for child in treeElement.children:
        find_paths(good, child, list(originalPath), list(originalPathSupport), pathArray)

    return True

def find_shortest_path(good, numberOfGoods):

    if not good.children:
        return ([good.name], 1)
    minLength = numberOfGoods
    minPath = []
    for child in good.children:
        (path, length) = find_shortest_path(child, numberOfGoods)
        path.append(child.name)
        length += 1
        if length < minLength:
            minLength = length
            minPath = path

    return (minPath, minLength)

if __name__ == "__main__":

    dataFileName = sys.argv[1]
    minSupport = float(sys.argv[2])

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

    arrayOfCommonSets = dict()
    for eachElement, support in commonGoodsSet.items():
        pathArray = dict()
        element = list(eachElement)[0]
        find_paths(element, fpTree.root, [], [], pathArray)
        newCommonGoodsArray = dict()
        for eachGood in commonGoodsSet.keys():
            good = list(eachGood)[0]
            for path, index in pathArray.items():
                pathList = list(path[0])
                supportList = list(path[1])
                if good in pathList:
                    placeOfGood = pathList.index(good)
                    supportOfGood = supportList[placeOfGood]
                    if tuple([good]) in newCommonGoodsArray:
                        newCommonGoodsArray[tuple([good])] += supportOfGood / float(numTransactions)
                    else:
                        newCommonGoodsArray[tuple([good])] = supportOfGood / float(numTransactions)

        sortNewCommonGoodsArray = sorted(newCommonGoodsArray.items(), key=operator.itemgetter(1), reverse=True)

        newTransactionsArray = []
        for path, index in pathArray.items():
            newTransaction = []
            pathList = list(path[0])
            for good in range(numGoods):
                if good in pathList:
                    newTransaction.append(1)
                else:
                    newTransaction.append(0)

            newTransactionsArray.append(newTransaction)

        sortNewData = sort_transactions(newTransactionsArray, sortNewCommonGoodsArray)
        nominalFpTree = Tree()
        build_fp_tree(nominalFpTree, sortNewData)

        for good, support in sortNewCommonGoodsArray:
            if support < minSupport:
                continue

            goodElement = list(good)[0]
            flag = False
            for child in nominalFpTree.root.children:
                if child.name == goodElement:
                    flag = True
                    (path, length) = find_shortest_path(child, numGoods)
                    path.append(element)
                    arrayOfCommonSets[tuple(path)] = support
                    break

            if not flag:
                arrayOfCommonSets[goodElement, element] = support

    for eachSet, support in arrayOfCommonSets.items():
        print eachSet, ':', support













