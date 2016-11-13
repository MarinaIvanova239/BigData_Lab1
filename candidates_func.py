import common

def remove_excess_sets(candidateSet, previousCommonGoodsSet):

    betterCandidateSet = []
    lengthOfCandidates = len(candidateSet[0])

    previousCommonGoodsArraySet = []
    for eachSet in previousCommonGoodsSet:
        previousCommonGoodsArraySet.append(list(eachSet))

    for eachCandidate in candidateSet:
        counter = 0
        listOfSubsets = common.get_subsets(eachCandidate)
        for subset in listOfSubsets:
            if subset in previousCommonGoodsArraySet:
                counter += 1

        if counter == lengthOfCandidates:
            betterCandidateSet.append(eachCandidate)

    return betterCandidateSet

def candidates_generation(previousCommonGoods, numberOfGoods):

    newCandidates = []
    if not previousCommonGoods:
        return []
    sizeOfGoodSet = len(previousCommonGoods[0])
    index = 0
    for good in previousCommonGoods:
        lastElement = good[sizeOfGoodSet - 1]
        for j in range(lastElement + 1, numberOfGoods):
            newCandidates.append(list(good))
            newCandidates[index].append(j)
            index += 1

    newCandidates = remove_excess_sets(newCandidates, previousCommonGoods)
    return newCandidates

def is_subset(candidate, transaction):

    counter = 0
    candidateLength = len(candidate)
    transactionLength = len(transaction)
    for element in candidate:
        if element > transactionLength:
            return False
        if transaction[element] > 0:
            counter += 1

    if counter == candidateLength:
        return True

    return False

def count_candidates_support(candidateSet, transactions, numberOfTransactions):

    candidatesWithSupport = dict()
    for candidate in candidateSet:
        candidatesWithSupport[tuple(candidate)] = 0
        for transaction in transactions:
            if is_subset(candidate, transaction):
                candidatesWithSupport[tuple(candidate)] += 1

        candidatesWithSupport[tuple(candidate)] /= float(numberOfTransactions)

    return candidatesWithSupport

def get_proper_set(commonRules, minSupport):

    commonRulesItems = commonRules.items()
    for key, value in commonRulesItems:
        if value < minSupport:
            del commonRules[key]

    return