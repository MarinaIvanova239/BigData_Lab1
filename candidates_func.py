import common

def remove_excess_sets(candidateSet, previousCommonGoodsSet):

    betterCandidateSet = []
    lengthOfCandidates = len(candidateSet[0])

    # extract sets from dict of previous common goods
    previousCommonGoodsArraySet = []
    for eachSet in previousCommonGoodsSet:
        previousCommonGoodsArraySet.append(list(eachSet))

    # check if candidate should be used later in algorithm
    for eachCandidate in candidateSet:
        counter = 0
        listOfSubsets = common.get_subsets(eachCandidate)
        # check if subset is in array of previous common goods
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
    # loop for set
    for good in previousCommonGoods:
        lastElement = good[sizeOfGoodSet - 1]
        # add to set goods which are after current in list of all goods
        for j in range(lastElement + 1, numberOfGoods):
            newCandidates.append(list(good))
            newCandidates[index].append(j)
            index += 1

    # remove sets in which at least one subset is not in array of previous common goods
    newCandidates = remove_excess_sets(newCandidates, previousCommonGoods)
    return newCandidates

def is_subset(candidate, transaction):

    counter = 0
    candidateLength = len(candidate)
    transactionLength = len(transaction)
    # check if each element of candidate is in transaction
    for element in candidate:
        if element > transactionLength:
            return False
        if transaction[element] > 0:
            counter += 1

    # if all elements of candidate are in transaction, return true
    if counter == candidateLength:
        return True

    return False

def count_candidates_support(candidateSet, transactions, numberOfTransactions):

    candidatesWithSupport = dict()
    # find support for each candidate from candidate set
    for candidate in candidateSet:
        candidatesWithSupport[tuple(candidate)] = 0
        # count support of candidate set
        for transaction in transactions:
            if is_subset(candidate, transaction):
                candidatesWithSupport[tuple(candidate)] += 1

        candidatesWithSupport[tuple(candidate)] /= float(numberOfTransactions)

    return candidatesWithSupport

def get_proper_set(commonSets, minSupport):

    commonSetsItems = commonSets.items()
    # delete set if it has support less than minSupport
    for key, value in commonSetsItems:
        if value < minSupport:
            del commonSets[key]

    return