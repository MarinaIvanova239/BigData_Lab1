import sys
import common
import time
import candidates_func

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

    commonRules = dict()
    numCommonSets = len(arrayOfCommonSets)
    for i in range(1, numCommonSets):
        commonSetItems = arrayOfCommonSets[i].items()
        for key, value in commonSetItems:
            common.get_common_rules(commonRules, arrayOfCommonSets, list(key), value, minConf, list(key))

    endTime = time.time()

    print 'items:'
    for commonSet in arrayOfCommonSets:
        for element, support in commonSet.items():
            print element, ':', support

    print '.......'
    print 'rules:'
    for eachRule, conf in commonRules.items():
        print eachRule, ':', conf

    print '.......'
    print 'time=', endTime - startTime


