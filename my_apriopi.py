import sys
import common
import time
import candidates_func

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

    allSubsets = common.get_subsets(oneSet)
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

    startTime = time.time()

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
        if support >= minSupport:
            commonGoodsSet[tuple([i])] = support

    candidateSet = []
    while commonGoodsSet:
        arrayOfCommonSets.append(commonGoodsSet)
        candidateSet = candidates_func.candidates_generation(commonGoodsSet.keys(), numGoods)
        commonGoodsSet = candidates_func.count_candidates_support(candidateSet, data, numTransactions)
        candidates_func.get_proper_set(commonGoodsSet, minSupport)

    print 'items:'
    for commonSet in arrayOfCommonSets:
        for element, support in commonSet.items():
            print element, ':', support

    commonRules = dict()
    numCommonSets = len(arrayOfCommonSets)
    for i in range(1, numCommonSets):
        commonSetItems = arrayOfCommonSets[i].items()
        for key, value in commonSetItems:
            get_common_rules(commonRules, arrayOfCommonSets, list(key), value, minConf, list(key))

    endTime = time.time()

    print '.......'
    print 'rules:'
    for eachRule, conf in commonRules.items():
        print eachRule, ':', conf

    print '.......'
    print 'time=', endTime - startTime


