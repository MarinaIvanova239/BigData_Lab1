import sys
import common

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


def remove_excess_rules(candidateSet, previousCommonGoodsSet):

    betterCandidateSet = []
    lengthOfCandidates = len(candidateSet[0])

    previousCommonGoodsArraySet = []
    for eachSet in previousCommonGoodsSet:
        previousCommonGoodsArraySet.append(list(eachSet))

    for eachCandidate in candidateSet:
        counter = 0
        listOfSubsets = get_subsets(eachCandidate)
        for subset in listOfSubsets:
            if subset in previousCommonGoodsArraySet:
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

    return

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
        commonGoodsSet[tuple([i])] = support

    candidateSet = []
    while commonGoodsSet:
        arrayOfCommonSets.append(commonGoodsSet)
        candidateSet = candidates_generation(commonGoodsSet.keys(), numGoods)
        commonGoodsSet = count_candidates_support(candidateSet, data, numTransactions)
        get_proper_set(commonGoodsSet, minSupport)

    commonRules = dict()
    numCommonSets = len(arrayOfCommonSets)
    for i in range(1, numCommonSets):
        commonSetItems = arrayOfCommonSets[i].items()
        for key, value in commonSetItems:
            get_common_rules(commonRules, arrayOfCommonSets, list(key), value, minConf, list(key))

    for eachRule, conf in commonRules.items():
        print eachRule, ':', conf


