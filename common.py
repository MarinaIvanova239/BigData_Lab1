import numpy as np

def get_dataset_from_csv_file(fileName):

    dataSet = []
    with open(fileName, 'rb') as csvfile:
        # read each line in csv file
        for line in csvfile.readlines():
            transactionString = line.split(',')
            # delete first element from transaction string - number of transaction
            transactionString = np.delete(transactionString, np.s_[0:1], axis=0)
            numGoods = transactionString.size
            transaction = []
            # add result to transaction array
            for i in range(numGoods):
                transaction.append(int(transactionString[i]))
            dataSet.append(transaction)

    return dataSet

def count_good_support(good, transactions, numberOfTransactions):

    # if good not in transaction list, return 0
    transactionsWithGood = 0
    if (len(transactions[0]) < good):
        return 0

    # count number of transactions which contain good
    for transaction in transactions:
        if transaction[good] > 0:
            transactionsWithGood = transactionsWithGood + 1

    # count good support
    goodSupport = transactionsWithGood / float(numberOfTransactions)
    return goodSupport

def get_subsets(set):

    arrayOfSubsets = []
    lengthOfSet = len(set)
    # find all subsets that have size = lengthOfSet - 1
    for j in range(lengthOfSet):
        if j == 0:
            shift = 0
            border = lengthOfSet - 1
        else:
            shift = j - 1
            border = lengthOfSet

        subset = []
        for i in range(0, shift):
            subset.append(set[i])
        for i in range(j, border):
            subset.append(set[i])

        arrayOfSubsets.append(subset)

    return arrayOfSubsets

def find_subset_support(subset, subsetSize, commonSets):

    # get support of subset from commonSets array
    commonSetsWithProperSize = commonSets[subsetSize - 1]
    support = commonSetsWithProperSize[tuple(subset)]

    return support

def find_rest_part(subset, wholeSet):

    restPart = []
    # find complement of subset
    for eachElement in wholeSet:
        if eachElement not in subset:
            restPart.append(eachElement)

    return restPart

def get_common_rules(commonRules, commonSets, oneSet, support, minConf, wholeSet):

    allSubsets = get_subsets(oneSet)
    sizeOfSubset = len(allSubsets[0])
    # loop for each subset of set
    for eachSubset in allSubsets:
        # count support and confidence of subset
        subsetSupport = find_subset_support(eachSubset, sizeOfSubset, commonSets)
        restPart = find_rest_part(eachSubset, wholeSet)
        conf = support / float(subsetSupport)

        # if subset has size = 1, recursion is not needed
        if sizeOfSubset == 1:
            if conf >= minConf:
                commonRules[(tuple(eachSubset), tuple(restPart))] = conf
            continue

        # find common rules for sets of greater size
        get_common_rules(commonRules, commonSets, eachSubset, support, minConf, wholeSet)

        # add rule only if confidence is more than minConf
        if conf >= minConf:
            commonRules[(tuple(eachSubset), tuple(restPart))] = conf

    return True
