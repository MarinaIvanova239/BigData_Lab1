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
    for eachTransaction in transactions:
        if eachTransaction[good] > 0:
            transactionsWithGood = transactionsWithGood + 1

    goodSupport = transactionsWithGood / float(numberOfTransactions)
    return goodSupport

def remove_excess_rules(candidateSet, previousCommonGoodsSet):

    betterCandidateSet = []
    lengthOfCandidates = len(candidateSet[0])

    previousCommonGoodsArraySet = []
    for eachSet in previousCommonGoodsSet:
        previousCommonGoodsArraySet.append(list(eachSet))

    for eachCandidate in candidateSet:
        counter = 0
        for j in range(lengthOfCandidates):
            if j == 0:
                shift = 0
                border = lengthOfCandidates - 1
            else:
                shift = j - 1
                border = lengthOfCandidates

            subSet = [elem for elem in eachCandidate if eachCandidate.index(elem) in range(j, border)
                      or eachCandidate.index(elem) in range(0, shift)]
            if subSet in previousCommonGoodsArraySet:
                counter += 1

        if counter == lengthOfCandidates:
            betterCandidateSet.append(eachCandidate)

    return betterCandidateSet

def candidates_generation(previousCommonGoods, numberOfGoods):

    newCandidates = []
    sizeOfSet = len(previousCommonGoods[0])
    index = 0
    for commonGood in previousCommonGoods:
        lastElement = commonGood[sizeOfSet - 1]
        for j in range(lastElement + 1, numberOfGoods):
            newCandidates.append(list(commonGood))
            newCandidates[index].append(j)
            index += 1

    newCandidates = remove_excess_rules(newCandidates, previousCommonGoods)
    return newCandidates

def is_subset(candidate, transaction):

    counter = 0
    candidateLength = len(candidate)
    for eachElement in candidate:
        if transaction[eachElement] > 0:
            counter += 1

    if counter == candidateLength:
        return True

    return False

def count_candidates_support(candidateSet, transactions, numberOfTransactions):

    candidatesWithSupport = dict()
    for eachCandidate in candidateSet:
        candidatesWithSupport[tuple(eachCandidate)] = 0

    for eachTransaction in transactions:
        for eachCandidate in candidateSet:
            if is_subset(eachCandidate, eachTransaction):
                candidatesWithSupport[tuple(eachCandidate)] += 1

    for eachCandidate in candidateSet:
        candidatesWithSupport[tuple(eachCandidate)] /= float(numberOfTransactions)

    return candidatesWithSupport

def get_proper_set(commonRules, minSupport):

    commonRulesItems = commonRules.items()
    for key, value in commonRulesItems:
        if value < minSupport:
            del commonRules[key]

    return None

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
    while commonGoodsSet:
        candidateSet = candidates_generation(commonGoodsSet.keys(), numGoods)
        commonGoodsSet = count_candidates_support(candidateSet, data, numTransactions)
        get_proper_set(commonGoodsSet, minSupport)
        arrayOfCommonSets.append(commonGoodsSet)

    numIterations = len(arrayOfCommonSets)
    print numIterations
