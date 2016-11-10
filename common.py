import numpy as np

def parse_csv_dataset(fileName):

    dataSet = []
    with open(fileName, 'rb') as csvfile:
        for line in csvfile.readlines():
            transactionString = line.split(',')
            transactionString = np.delete(transactionString, np.s_[0:1], axis=0)
            numGoods = transactionString.size
            transaction = []
            for i in range(numGoods):
                transaction.append(int(transactionString[i]))
            dataSet.append(transaction)

    return dataSet

def count_good_support(good, transactions, numberOfTransactions):

    transactionsWithGood = 0
    for transaction in transactions:
        if transaction[good] > 0:
            transactionsWithGood = transactionsWithGood + 1

    goodSupport = transactionsWithGood / float(numberOfTransactions)
    return goodSupport

def get_subsets(set):

    arrayOfSubsets = []
    lengthOfSet = len(set)
    for j in range(lengthOfSet):
        if j == 0:
            shift = 0
            border = lengthOfSet - 1
        else:
            shift = j - 1
            border = lengthOfSet

        subset = [elem for elem in set if set.index(elem) in range(j, border)
                  or set.index(elem) in range(0, shift)]
        arrayOfSubsets.append(subset)

    return arrayOfSubsets

def find_subset_support(subset, subsetSize, commonSets):

    commonSetsWithProperSize = commonSets[subsetSize - 1]
    support = commonSetsWithProperSize[tuple(subset)]

    return support

def find_rest_part(subset, wholeSet):

    restPart = []
    for eachElement in wholeSet:
        if eachElement not in subset:
            restPart.append(eachElement)

    return restPart

def get_common_rules(commonRules, commonSets, oneSet, support,  minConf, wholeSet):

    allSubsets = get_subsets(oneSet)
    sizeOfSubset = len(allSubsets[0])
    for eachSubset in allSubsets:
        subsetSupport = find_subset_support(eachSubset, sizeOfSubset, commonSets)
        restPart = find_rest_part(eachSubset, wholeSet)
        conf = support / float(subsetSupport)
        if sizeOfSubset == 1:
            if conf >= minConf:
                commonRules[(tuple(eachSubset), tuple(restPart))] = conf
            return True

        get_common_rules(commonRules, commonSets, eachSubset, support, minConf, wholeSet)
        if conf >= minConf:
            commonRules[(tuple(eachSubset), tuple(restPart))] = conf

    return True
