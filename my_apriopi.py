import sys
import numpy as np

def parse_csv_dataset(fileName):

    dataSet = []
    with open(fileName, 'rb') as csvfile:

        for line in csvfile.readlines():
            rowAsString = line.split(',')
            rowAsString = np.delete(rowAsString, np.s_[0:1], axis=0)
            numElements = rowAsString.size
            rowAsInt = []
            for i in range(numElements):
                rowAsInt.append(int(rowAsString[i]))

            dataSet.append(rowAsInt)

    return dataSet

def count_good_support(good, transactions, numberOfTransactions):

    transactionsWithGood = 0
    for each_transaction in (transactions):
        if each_transaction[good] > 0:
            transactionsWithGood = transactionsWithGood + 1

    goodSupport = transactionsWithGood / numberOfTransactions
    return goodSupport

def remove_excess_rules(candidateSet, previousCommonGoodsSet):

    betterCandidateSet = []
    numberOfCandidates = len(candidateSet)
    lengthOfCandidates = len(candidateSet[0])

    for i in range(numberOfCandidates):
        counter = 0
        for j in range(lengthOfCandidates):
            if j == 0:
                shift = 0
                border = lengthOfCandidates - 1
            else:
                shift = j - 1
                border = lengthOfCandidates

            subSet = [elem for elem in candidateSet if candidateSet.index(elem) in range(j, border)
                      or candidateSet.index(elem) in range(0, shift)]
            if subSet in previousCommonGoodsSet:
                counter = counter + 1

        if counter == lengthOfCandidates:
            betterCandidateSet.append(candidateSet[i])

    return betterCandidateSet

def candidates_generation(previousCommonGoods, numberOfGoods):

    newCandidates = []
    sizeOfPreviousCandidateSet = len(previousCommonGoods)
    index = 0
    for i in range(sizeOfPreviousCandidateSet):
        for j in range(i + 1, numberOfGoods):
            newCandidates.append(list(previousCommonGoods[i]))
            newCandidates[index].append(j)
            index = index + 1

    newCandidates = remove_excess_rules(newCandidates, previousCommonGoods)
    return newCandidates

def count_candidates_support(candidateSet, transactions, numberOfTransactions):

    candidatesWithSupport = dict()
    # for eachTransaction in range(transactions):
    # support = counter / numberOfTransactions
    # candidatesWithSupport[tuple(candidateSet[i])] = support

    return candidatesWithSupport

def get_proper_set(commonRules):

    properSet = []
    return properSet

if __name__ == "__main__":

    dataFileName = sys.argv[1]
    minSupport = float(sys.argv[2])

    data = parse_csv_dataset(dataFileName)
    numTransactions = len(data)
    numGoods = len(data[0])

    arrayOfCommonSets = []
    commonGoodsSet = dict()
    for i in range(numGoods):
        support = count_good_support(i, data, numTransactions)
        commonGoodsSet[tuple([i])] = support

    arrayOfCommonSets.append(commonGoodsSet)

    candidateSet = []
    for k in range(1):
    #while commonGoodsSet:
        candidateSet = candidates_generation(commonGoodsSet.keys(), numGoods)
        commonGoodsSet = count_candidates_support(candidateSet, data, numTransactions)
        commonGoodsSet = get_proper_set(commonGoodsSet)
        arrayOfCommonSets.append(commonGoodsSet)

